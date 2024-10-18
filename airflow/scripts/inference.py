
import torch
import faiss
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
from vectorize_data import vectorizer

# Load FAISS index
index = faiss.read_index("../vector_db/vector_database.faiss")
vec = vectorizer()
# Function to retrieve relevant data from FAISS using input query
def retrieve_relevant_data(query_embedding, top_k=2):
    D, I = index.search(query_embedding, top_k)  # Get top K nearest vectors
    return I  # Return indices of relevant data (modify as per your actual data retrieval process)
quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
# Load the LLM model for inference
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cuda",
    torch_dtype=torch.float16,
    use_flash_attention=True,
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    quantization_config=quantization_config,
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

# Initialize the conversation loop
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 500,
    "return_full_text": False,
    "temperature": 0.5,
    "do_sample": True,
}

# Start conversation loop
def start_conversation():
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    while True:
        # Get user input
        user_input = input("User: ")

        # Break the loop if the user says 'exit'
        if user_input.lower() == "exit":
            print("Exiting conversation...")
            break

        with torch.no_grad():
            query_embedding = vec.get_embeddings(user_input)

        # Retrieve relevant data from FAISS
        relevant_indices = retrieve_relevant_data(query_embedding)
        # Here, you'd fetch the corresponding text data for the retrieved indices to augment the response
        retrieved_text = " ".join([f"Relevant info {i}" for i in relevant_indices])  # Replace with actual data

        # Add the retrieved context to the conversation
        messages.append({"role": "user", "content": user_input+retrieved_text})

        # Generate response
        output = pipe(messages, **generation_args)
        assistant_reply = output[0]["generated_text"]

        # Print the assistant's response
        print(f"Assistant: {assistant_reply}")

# Start the conversation loop
if __name__ == "__main__":
    start_conversation()
