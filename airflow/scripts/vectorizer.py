import json
import numpy as np
import faiss
import os

def load_json_to_faiss(json_folder, index_file):
    vectors = []
    ids = []

    # Read each JSON file from the scraped data folder
    for file_name in os.listdir(json_folder):
        if file_name.endswith(".json"):
            json_path = os.path.join(json_folder, file_name)

            # Load JSON data from file
            with open(json_path, 'r') as f:
                data = json.load(f)

            # Extract vectors and ids from each JSON entry
            for item in data:
                vector = np.array(item['vector'], dtype=np.float32)  # Ensure vector is a float32 numpy array
                vectors.append(vector)
                ids.append(item['id'])

    if len(vectors) == 0:
        print("No vectors found in the JSON files.")
        return

    # Convert the list of vectors to a 2D numpy array
    vectors = np.array(vectors, dtype=np.float32)

    # Create FAISS index (IndexFlatL2 is a simple L2 distance index)
    index = faiss.IndexFlatL2(len(vectors[0]))

    # Add vectors to the FAISS index
    index.add(vectors)

    # Save the FAISS index to a file
    faiss.write_index(index, index_file)

    print(f"FAISS index created and saved to {index_file}")
    print(f"Indexed IDs: {ids}")
