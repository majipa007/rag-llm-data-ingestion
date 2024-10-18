import faiss
import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np

# Load the LLM model (for embeddings)


# Sample data to vectorize (replace with scraped data)
texts = [
    "The first text to vectorize.",
    "Another example of data that will be vectorized.",
    "This is additional content for testing FAISS vector storage."
]

class vectorizer:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Use a suitable embedding model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def get_embeddings(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)  # Use mean pooling
        return embeddings.numpy()

v = vectorizer()
# Vectorize the data
embeddings = v.get_embeddings(texts)

# Create FAISS index
d = embeddings.shape[1]  # Dimensionality of the embeddings
index = faiss.IndexFlatL2(d)  # L2 distance metric

# Add vectors to the FAISS index
index.add(embeddings)

# Save the FAISS index
faiss.write_index(index, "../vector_db/vector_database.faiss")

print("Vector database saved successfully!")






