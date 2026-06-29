import trafilatura
import re

def fetch_article(url: str) -> dict | None:
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None

        text = trafilatura.extract(downloaded, include_tables=False, include_links=False)
        if not text or len(text) < 100:
            return None

        metadata = trafilatura.extract_metadata(downloaded)

        keywords = []
        if metadata:
            for attr in ("tags", "categories", "description"):
                val = getattr(metadata, attr, None)
                if val:
                    if isinstance(val, list):
                        keywords.extend(val)
                    elif isinstance(val, str) and val.strip():
                        keywords.extend([k.strip() for k in re.split(r"[,\s]+", val) if len(k.strip()) > 2])
            keywords = list(dict.fromkeys(kw.lower() for kw in keywords))[:20]

        return {
            "title": metadata.title if metadata and metadata.title else "",
            "text": text[:10000],
            "keywords": keywords,
        }

    except Exception:
        return None
