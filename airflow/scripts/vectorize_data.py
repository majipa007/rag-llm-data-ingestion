import faiss
import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np
import os

class Vectorizer:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def get_embeddings(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)  # Use mean pooling
        return embeddings.numpy()

def vectorize_and_save(input_path, output_path):
    # Load text from file
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    texts = text.split("\n\n")  # Assumes paragraphs are separated by double newlines
    
    # Vectorize the data
    vectorizer = Vectorizer()
    embeddings = vectorizer.get_embeddings(texts)

    # Create FAISS index
    d = embeddings.shape[1]  # Dimensionality of embeddings
    index = faiss.IndexFlatL2(d)  # L2 distance metric

    # Add vectors to the FAISS index
    index.add(embeddings)

    # Save the FAISS index
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    faiss.write_index(index, output_path)

    print("Vector database saved successfully at", output_path)

# # Example usage
# input_path = "/opt/airflow/Scrapped_data/data.txt"  # Path to scraped data
# output_path = "/opt/airflow/vector_db/vector_database.faiss"  # Path to save FAISS index
# vectorize_and_save(input_path, output_path)
