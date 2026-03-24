import os

documents = {
    "1_python_basics.txt": "Python is a high-level, interpreted programming language known for its readability. It is widely used in data science, web development, and automation.",
    "2_data_structures.txt": "Data structures like lists, dictionaries, sets, and tuples are essential in Python. A dictionary allows fast lookups using key-value pairs.",
    "3_search_algorithms.txt": "Search algorithms are step-by-step procedures used to locate specific data among a collection of data. Common ones include linear search and binary search.",
    "4_binary_search.txt": "Binary search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item.",
    "5_fastapi_intro.txt": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
    "6_react_frontend.txt": "React is a free and open-source front-end JavaScript library for building user interfaces based on components. It is maintained by Meta.",
    "7_inverted_index.txt": "An inverted index is an index data structure storing a mapping from content, such as words or numbers, to its locations in a document or a set of documents.",
    "8_time_complexity.txt": "In computer science, time complexity is the computational complexity that describes the amount of computer time it takes to run an algorithm.",
    "9_space_complexity.txt": "Space complexity refers to the total amount of memory space that an algorithm or program needs to execute and complete.",
    "10_hash_tables.txt": "A hash table is a data structure that implements an associative array abstract data type, a structure that can map keys to values using a hash function.",
    "11_graphs_and_trees.txt": "Graphs and trees are fundamental data structures. A tree is a special type of graph that is connected and acyclic.",
    "12_api_design.txt": "REST API design typically involves using standard HTTP methods like GET, POST, PUT, and DELETE to manage resources on the server.",
    "13_cors_explained.txt": "Cross-Origin Resource Sharing (CORS) is an HTTP-header based mechanism that allows a server to indicate any origins other than its own from which a browser should permit loading resources.",
    "14_sorting_algorithms.txt": "Sorting is a very common operation in computer science. Algorithms like merge sort, quick sort, and bubble sort arrange elements in a specific order.",
    "15_fullstack_dev.txt": "A full-stack developer is a professional who is proficient in both front-end and back-end web development, working with databases, servers, and clients."
}

os.makedirs("documents", exist_ok=True)
for filename, content in documents.items():
    with open(os.path.join("documents", filename), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(documents)} document files in the 'documents' directory.")
