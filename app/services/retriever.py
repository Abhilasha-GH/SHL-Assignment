import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# Load catalog
with open("data/cleaned_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Load FAISS index
index = faiss.read_index("data/shl_index.faiss")

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)

def search_assessments(query, top_k=5):

    # Convert query to embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(catalog):
            results.append(catalog[idx])

    return results