import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse, urlunparse
import time

BASE_URL = "https://www.geeksforgeeks.org/"
visited = set()
results = []

def normalize_url(url):
    """Normalize the URL by removing fragments and trailing slashes."""
    parsed = urlparse(url)
    clean = parsed._replace(query='', fragment='')
    return urlunparse(clean).rstrip('/')

def is_valid_algorithm_link(url):
    """Check if the link is likely algorithm-related (based on URL pattern)."""
    return ('algorithm' in url.lower()) and all(excl not in url for excl in ['shop', 'courses', '/category/uncategorized'])

def crawl(url, depth=1):
    normalized_url = normalize_url(url)
    if normalized_url in visited or depth <= 0:
        return
    visited.add(normalized_url)

    try:
        res = requests.get(normalized_url, timeout=10)
        if res.status_code != 200:
            return
        soup = BeautifulSoup(res.content, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            raw_href = a_tag['href']
            full_url = normalize_url(urljoin(BASE_URL, raw_href))
            title = a_tag.get_text(strip=True).split('\n')[0][:120]  # Truncate long titles

            if is_valid_algorithm_link(full_url) and title:
                if (title, full_url) not in results:
                    results.append((title, full_url))
                    print(f"[+] Found: {title}\n    {full_url}")

            if full_url not in visited and 'geeksforgeeks.org' in full_url:
                crawl(full_url, depth=depth - 1)

        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Error at {normalized_url}: {e}")

# Start crawling with safe depth
crawl(BASE_URL, depth=2)

# Save to CSV
df = pd.DataFrame(list(set(results)), columns=["Title", "URL"])
df.to_csv("gfg_cleaned_algorithm_articles.csv", index=False, encoding="utf-8")

print(f"\n✅ Done! Saved {len(df)} clean algorithm articles to 'gfg_cleaned_algorithm_articles.csv'")
