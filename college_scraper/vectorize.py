import json
import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    texts = []
    urls = []
    for entry in data:
        texts.extend(entry['text'])
        urls.extend([entry['url']] * len(entry['text']))
    return texts, urls

def encode_texts(texts, tokenizer, model, batch_size=32, device='cpu'):
    model.to(device)
    model.eval()
    embeddings = []
    with torch.no_grad():
        for i in tqdm(range(0, len(texts), batch_size), desc="Encoding texts"):
            batch_texts = texts[i:i+batch_size]
            encoded_input = tokenizer(batch_texts, padding=True, truncation=True, return_tensors='pt').to(device)
            model_output = model(**encoded_input)
            # Mean pooling
            embeddings_batch = model_output.last_hidden_state.mean(dim=1).cpu().numpy()
            embeddings.append(embeddings_batch)
    embeddings = np.vstack(embeddings)
    return embeddings

def main():
    # Paths
    json_file = "college_scraper/output"
    index_file = 'college_index.faiss'
    urls_file = 'urls.json'

    # Load data
    texts, urls = load_data(json_file)
    print(f"Loaded {len(texts)} text segments from {len(urls)} URLs.")

    # Initialize tokenizer and model
    model_name = "BAAI/bge-reranker-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # Determine device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Encode texts
    vectors = encode_texts(texts, tokenizer, model, device=device)
    print(f"Encoded texts into vectors of shape: {vectors.shape}")

    # Create FAISS index
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    print(f"FAISS index contains {index.ntotal} vectors.")

    # Save FAISS index
    faiss.write_index(index, index_file)
    print(f"FAISS index saved to {index_file}.")

    # Save URLs
    with open(urls_file, 'w') as f:
        json.dump(urls, f)
    print(f"URLs saved to {urls_file}.")

if __name__ == "__main__":
    main()
