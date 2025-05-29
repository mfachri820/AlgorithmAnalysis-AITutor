from sentence_transformers import SentenceTransformer
import pandas as pd
import pickle
import numpy as np

# Load your dataset
df = pd.read_csv("data/gfg_cleaned_algorithm_articles.csv")

# Use title for embedding
texts = df['Title'].tolist()

# Create embeddings using a small, efficient model
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts, show_progress_bar=True)

# Save embeddings for later use
with open("gfg_embeddings.pkl", "wb") as f:
    pickle.dump((texts, df['URL'].tolist(), embeddings), f)
