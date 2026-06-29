import requests
from bs4 import BeautifulSoup
import re

def fetch_article(url: str) -> dict | None:
    try:
        response = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        text = re.sub(r"\n\s*\n", "\n\n", text).strip()

        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)

        for selector in ["h1", "article h1", ".article-title", ".entry-title", "h1.entry-title"]:
            h1 = soup.select_one(selector)
            if h1:
                title = h1.get_text(strip=True)
                break

        publish_date = ""
        for tag in soup.find_all("time"):
            if tag.get("datetime"):
                publish_date = tag["datetime"]
                break

        authors = []
        for meta in soup.find_all("meta", attrs={"name": "author"}) or []:
            if meta.get("content"):
                authors.append(meta["content"])

        if len(text) < 100:
            return None

        return {
            "title": title,
            "text": text[:10000],
            "authors": authors,
            "publish_date": publish_date,
        }

    except Exception:
        return None
