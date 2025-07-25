from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Load dummy data
with open("data/dummy_text.json", "r") as f:
    documents = json.load(f)

# Embed documents
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index
os.makedirs("data", exist_ok=True)
faiss.write_index(index, "data/faiss_index.index")
