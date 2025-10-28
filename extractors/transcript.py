
from __future__ import annotations
from typing import List, Tuple, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def fetch_transcript_yta(video_id: str, languages: Optional[List[str]] = None) -> List[Tuple[float, float, str]]:
    """Return list of (start, duration, text) using youtube-transcript-api v1.x .fetch interface."""
    languages = languages or ["de", "en"]
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id, languages=languages)
        return [(snip.start, snip.duration, snip.text) for snip in fetched]
    except Exception:
        return []

def yt_video_id(url: str) -> str:
    return YouTube(url).video_id

def fetch_transcript_pytube(url: str, lang_priority: Optional[List[str]] = None) -> List[Tuple[float, float, str]]:
    lang_priority = lang_priority or ["de", "en"]
    try:
        yt = YouTube(url)
        if not yt.captions:
            return []
        tracks = list(yt.captions.keys())
        chosen = None
        for lp in lang_priority:
            for t in tracks:
                if lp in t.lower():
                    chosen = yt.captions.get_by_language_code(lp) or yt.captions[t]
                    break
            if chosen: break
        if not chosen:
            chosen = yt.captions[tracks[0]]
        xml = chosen.xml_captions
        import re, html
        entries = re.findall(r'<text start="([0-9\.]+)" dur="([0-9\.]+)">(.*?)</text>', xml)
        return [(float(s), float(d), html.unescape(t.replace("\n", " ").strip())) for s, d, t in entries]
    except Exception:
        return []

def list_available_transcripts(video_id: str):
    try:
        ytt_api = YouTubeTranscriptApi()
        tlist = ytt_api.list(video_id)
        return [{
            "language": t.language,
            "language_code": t.language_code,
            "is_generated": t.is_generated,
            "is_translatable": t.is_translatable,
        } for t in tlist]
    except Exception:
        return []

def get_video_title(url: str) -> Optional[str]:
    try:
        yt = YouTube(url)
        return yt.title
    except Exception:
        return None
