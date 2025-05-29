from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re

def looks_like_code(text):
    patterns = [
        r";", r"\b(int|float|double|char|void|for|while|if|else|return)\b",
        r"{.*}", r"#include\s*<.*>", r"def\s+\w+", r"class\s+\w+",
        r"public|private|protected", r"import\s+\w+", r"\(|\)"
    ]
    return any(re.search(p, text) for p in patterns)

# Load precomputed GFG embeddings
with open("data/gfg_embeddings.pkl", "rb") as f:
    titles, urls, embeddings = pickle.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_best_matches(query, top_n=3):
    query_vec = model.encode([query])
    similarities = cosine_similarity(query_vec, embeddings)[0]
    top_idx = np.argsort(similarities)[::-1][:top_n]
    return [(titles[i], urls[i]) for i in top_idx]
