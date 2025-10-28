
import re
from urllib.parse import urlparse, parse_qs

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-\_\s]", "", text)
    text = re.sub(r"[\s\_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-") or "video"

def slug_from_youtube_url(url: str) -> str:
    try:
        vid = parse_qs(urlparse(url).query).get("v", [None])[0]
        if vid:
            return slugify(vid)
        path = urlparse(url).path.strip("/")
        if path:
            return slugify(path.split("/")[-1])
    except Exception:
        pass
    return "video"
