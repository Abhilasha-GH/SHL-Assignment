import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# Load cleaned catalog
with open("data/cleaned_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create text for embeddings
texts = [
    f"{item['name']} {item['url']}"
    for item in catalog
]

# Generate embeddings
embeddings = model.encode(texts)

# Convert to numpy array
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# Save index
faiss.write_index(index, "data/shl_index.faiss")

print(f"Indexed {len(catalog)} assessments")