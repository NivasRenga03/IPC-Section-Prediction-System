import json
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

# Load structured IPC JSON file
with open(r"C:\Users\raji\Downloads\garbage_ml\structured_ipc (1).json", "r", encoding="utf-8") as f:
    ipc_data = json.load(f)

# Extract sections and descriptions
sections = [item["Description"] for item in ipc_data]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(sections)

# Sentence Transformer for FAISS
encoder_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = encoder_model.encode(sections, convert_to_numpy=True)

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

def search_ipc(query, top_k=5):
    """Search IPC sections using FAISS similarity."""
    query_embedding = encoder_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(ipc_data):
            results.append({
                "Section": ipc_data[idx]["Section"],
                "Offence": ipc_data[idx]["Offence"],
                "Description": ipc_data[idx]["Description"],
                "Similarity": float(1 - distances[0][i])
            })
    return results
import json
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

# Load structured IPC JSON file
with open(r"C:\Users\raji\Downloads\garbage_ml\structured_ipc (1).json", "r", encoding="utf-8") as f:
    ipc_data = json.load(f)

# Extract sections and descriptions
sections = [item["Description"] for item in ipc_data]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(sections)

# Sentence Transformer for FAISS
encoder_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = encoder_model.encode(sections, convert_to_numpy=True)

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

def search_ipc(query, top_k=5):
    """Search IPC sections using FAISS similarity."""
    query_embedding = encoder_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(ipc_data):
            results.append({
                "Section": ipc_data[idx]["Section"],
                "Offence": ipc_data[idx]["Offence"],
                "Description": ipc_data[idx]["Description"],
                "Similarity": float(1 - distances[0][i])
            })
    return results
