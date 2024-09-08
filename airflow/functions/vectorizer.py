import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load pre-trained SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def load_json_to_faiss(json_file, faiss_index_file):
    try:
        # Load the scraped data from the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Error loading JSON file: {e}")
        return

    # Convert the texts into vectors using the pre-trained SentenceTransformer model
    texts = [entry['text'] for entry in data]
    try:
        vectors = model.encode(texts)
    except Exception as e:
        logger.error(f"Error encoding texts to vectors: {e}")
        return

    vectors_np = np.array(vectors).astype('float32')
    dim = vectors_np.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dim)
    index.add(vectors_np)

    try:
        # Save FAISS index to file
        faiss_index_file.parent.mkdir(parents=True, exist_ok=True)  # Create folder if doesn't exist
        faiss.write_index(index, str(faiss_index_file))
    except IOError as e:
        logger.error(f"Error saving FAISS index to file: {e}")
        return

    logger.info(f"FAISS index saved to {faiss_index_file}")
