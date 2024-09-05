import json
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import numpy as np

def vectorize_and_store_json(json_file_path, db_path):
    # Read JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Convert JSON to string for vectorization
    text = json.dumps(data)
    
    # Vectorize the text using CountVectorizer
    vectorizer = CountVectorizer()
    vector = vectorizer.fit_transform([text])
    
    # Convert sparse matrix to dense array
    dense_vector = vector.toarray()[0]
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS vectors
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       vector BLOB)''')
    
    # Store the vector in the database
    vector_bytes = dense_vector.tobytes()
    cursor.execute("INSERT INTO vectors (vector) VALUES (?)", (vector_bytes,))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Vector stored successfully in {db_path}")

# Example usage
# vectorize_and_store_json('path/to/your/json/file.json', 'path/to/your/vector/database.db')