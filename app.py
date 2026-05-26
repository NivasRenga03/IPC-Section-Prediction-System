from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

# Load IPC Data
json_path = r"C:\Users\raji\Downloads\garbage_ml\ipc.json"
with open(json_path, "r", encoding="utf-8") as f:
    ipc_data = json.load(f)

# Extract section descriptions for embedding
sections = [item["section_desc"] for item in ipc_data]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(sections)

# Sentence Transformer for FAISS
encoder_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = encoder_model.encode(sections, convert_to_numpy=True)

# Create FAISS Index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

@app.route("/")
def home():
    """Serve the frontend HTML page."""
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search_ipc():
    """Search IPC sections using FAISS similarity."""
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Encode query and search in FAISS index
    query_embedding = encoder_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, 5)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(ipc_data):
            results.append({
                "Chapter": ipc_data[idx]["chapter_title"],
                "Section": ipc_data[idx]["Section"],
                "Title": ipc_data[idx]["section_title"],
                "Description": ipc_data[idx]["section_desc"],
                "Similarity": float(1 - distances[0][i])  # Convert L2 distance to similarity score
            })

    return jsonify(results if results else {"message": "No matching sections found."})

if __name__ == "__main__":
    app.run(debug=True)
