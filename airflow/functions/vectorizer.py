import json
import numpy as np
import faiss

def load_json_to_faiss(json_file, index_file):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract vectors and ids
    vectors = []
    ids = []
    for item in data:
        vectors.append(np.array(item['vector']))
        ids.append(item['id'])

    # Convert to numpy array
    vectors = np.array(vectors, dtype=np.float32)

    # Create Faiss index
    index = faiss.IndexFlatL2(len(vectors[0]))

    # Add vectors to the index
    index.add(vectors)

    # Save index to file
    faiss.write_index(index, index_file)

    print( index, ids)