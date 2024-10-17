import faiss
import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np

# Load the LLM model (for embeddings)
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Use a suitable embedding model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Sample data to vectorize (replace with scraped data)
texts = [
    "The first text to vectorize.",
    "Another example of data that will be vectorized.",
    "This is additional content for testing FAISS vector storage."
]

# Function to generate embeddings
def get_embeddings(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # Use mean pooling
    return embeddings

# Vectorize the data
embeddings = get_embeddings(texts).numpy()

# Create FAISS index
d = embeddings.shape[1]  # Dimensionality of the embeddings
index = faiss.IndexFlatL2(d)  # L2 distance metric

# Add vectors to the FAISS index
index.add(embeddings)

# Save the FAISS index
faiss.write_index(index, "../vector_db/vector_database.faiss")

print("Vector database saved successfully!")

