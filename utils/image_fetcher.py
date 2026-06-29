import os
import requests
import re

UNSPLASH_API = "https://api.unsplash.com/search/photos"

def extract_keywords(text: str, max_words: int = 3) -> str:
    words = re.findall(r'\b[a-zA-Z\u0600-\u06FF]{4,}\b', text)
    seen = set()
    unique = []
    for w in words:
        if w.lower() not in seen:
            seen.add(w.lower())
            unique.append(w)
    return " ".join(unique[:max_words])

def fetch_image_for_post(post_text: str) -> str | None:
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        return None

    query = extract_keywords(post_text)
    if not query:
        return None

    try:
        response = requests.get(
            UNSPLASH_API,
            params={"query": query, "per_page": 1, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {access_key}"},
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                return data["results"][0]["urls"]["regular"]
        return None
    except Exception:
        return None
