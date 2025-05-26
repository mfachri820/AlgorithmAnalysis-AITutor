import pandas as pd
from fuzzywuzzy import fuzz

def load_gfg_links(csv_path="data/gfg_links.csv"):
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return pd.DataFrame(columns=["topic", "link"])

def find_link_from_csv(query, df, threshold=70):
    query_lower = query.lower()
    best_match = None
    best_score = 0

    for _, row in df.iterrows():
        topic = row["topic"].lower()
        score = fuzz.partial_ratio(query_lower, topic)
        if score > best_score and score >= threshold:
            best_match = row["link"]
            best_score = score

    return best_match or ""
