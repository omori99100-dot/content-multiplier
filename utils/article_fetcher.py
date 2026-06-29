import requests
from bs4 import BeautifulSoup
from newspaper import Article
import re

def fetch_article(url: str) -> dict | None:
    try:
        article = Article(url)
        article.download()
        article.parse()

        if article.text and len(article.text) > 100:
            return {
                "title": article.title or "",
                "text": article.text,
                "authors": article.authors,
                "publish_date": str(article.publish_date) if article.publish_date else "",
            }

        response = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        text = re.sub(r"\n\s*\n", "\n\n", text).strip()

        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)

        if len(text) < 100:
            return None

        return {"title": title, "text": text[:10000], "authors": [], "publish_date": ""}

    except Exception as e:
        return None
