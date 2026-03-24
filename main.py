from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import re
from collections import defaultdict, Counter
from typing import List

class SimpleSearchEngine:
    def __init__(self):
        # Store documents: {filename: content}
        self.documents = {}

        # Inverted index: {word: set(filenames)}
        self.index = defaultdict(set)

    def load_documents_from_folder(self, folder_path):
        """Load all .txt files from a folder."""
        if not os.path.exists(folder_path):
            raise ValueError("Folder does not exist.")

        loaded_count = 0
        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    self.documents[file] = content
                    self._index_document(file, content)
                    loaded_count += 1
        return loaded_count
        
    def load_document(self, filename, content):
        """Index a single document content."""
        content = content.lower()
        self.documents[filename] = content
        self._index_document(filename, content)

    def _index_document(self, filename, content):
        """Create inverted index for fast searching."""
        words = re.findall(r'\w+', content)  # Extract words
        for word in words:
            self.index[word].add(filename)

    def search(self, query):
        """Search for documents containing the query words."""
        query_words = re.findall(r'\w+', query.lower())

        if not query_words:
            return []

        # Find documents containing ALL query words
        result_docs = None

        for word in query_words:
            if word in self.index:
                if result_docs is None:
                    result_docs = self.index[word].copy()
                else:
                    result_docs &= self.index[word]  # Intersection
            else:
                result_docs = set()
                break

        if not result_docs:
            return []

        # Rank documents by frequency
        ranked_results = []
        for doc in result_docs:
            word_counts = Counter(re.findall(r'\w+', self.documents[doc]))
            score = sum(word_counts[word] for word in query_words)
            ranked_results.append({"document": doc, "score": score})

        # Sort by frequency (highest first)
        ranked_results.sort(key=lambda x: x["score"], reverse=True)
        return ranked_results

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-load documents on startup
    folder = "documents"
    if os.path.exists(folder):
        try:
            count = engine.load_documents_from_folder(folder)
            print(f"Startup: Loaded {count} documents from '{folder}'.")
        except Exception as e:
            print(f"Startup: Error loading documents: {e}")
    yield

app = FastAPI(title="Search Engine API", lifespan=lifespan)

# Add CORS middleware to allow the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production, e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the search engine
engine = SimpleSearchEngine()

class FolderLoadRequest(BaseModel):
    folder_path: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Search Engine API is running.", "status": 200}

@app.post("/login")
def login(request: LoginRequest):
    """Simulate a user login using dummy database."""
    users_file = os.path.join("database", "users.json")
    if not os.path.exists(users_file):
        raise HTTPException(status_code=500, detail="User database not found.")
        
    try:
        with open(users_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            users = data.get("users", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading database: {str(e)}")

    for user in users:
        if user["username"] == request.username and user["password"] == request.password:
            # Return user details without password
            return {
                "message": "Login successful",
                "user": {
                    "id": user.get("id"),
                    "username": user.get("username"),
                    "name": user.get("name")
                }
            }
            
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/load_folder")
def load_folder(request: FolderLoadRequest):
    """Endpoint to load text files from a local folder on the server."""
    # Convert backslashes to forward slashes just in case
    folder_path = request.folder_path.replace("\\", "/")
    
    try:
        count = engine.load_documents_from_folder(folder_path)
        return {"message": f"{count} documents loaded successfully from {folder_path}."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/upload_documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Endpoint to upload .txt files directly via API (very useful for React)."""
    loaded_count = 0
    for file in files:
        if file.filename.endswith(".txt"):
            content = await file.read()
            text_content = content.decode('utf-8', errors='ignore')
            engine.load_document(file.filename, text_content)
            loaded_count += 1
    return {"message": f"{loaded_count} documents uploaded and loaded successfully."}

@app.get("/search")
def search(query: str):
    """Endpoint to search for keywords in loaded documents."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    results = engine.search(query)
    return {
        "query": query,
        "total_results": len(results),
        "results": results
    }

@app.get("/documents")
def get_documents_status():
    """Endpoint to check which documents are currently loaded."""
    return {
        "total_documents": len(engine.documents),
        "documents": list(engine.documents.keys())
    }

@app.get("/documents/{filename}")
def get_document_content(filename: str):
    """Endpoint to get the content of a specific document."""
    if filename not in engine.documents:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {
        "filename": filename,
        "content": engine.documents[filename]
    }