
from __future__ import annotations
from typing import List, Tuple, Optional
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from pytube import YouTube

def fetch_transcript_yta(video_id: str, languages: Optional[List[str]] = None) -> List[Tuple[float, float, str]]:
    """Returns list of (start, duration, text)."""
    languages = languages or ["de", "en"]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return [(seg.get("start", 0.0), seg.get("duration", 0.0), seg.get("text", "")) for seg in transcript]
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return []

def yt_video_id(url: str) -> str:
    # Robust-ish extraction via pytube
    return YouTube(url).video_id

def fetch_transcript_pytube(url: str, lang_priority: Optional[List[str]] = None) -> List[Tuple[float, float, str]]:
    lang_priority = lang_priority or ["de", "en"]
    try:
        yt = YouTube(url)
        if not yt.captions:
            return []
        # Try priority languages, else first available
        tracks = list(yt.captions.keys())
        chosen = None
        for lp in lang_priority:
            for t in tracks:
                if lp in t.lower():
                    chosen = yt.captions.get_by_language_code(lp) or yt.captions[t]
                    break
            if chosen: break
        if not chosen:
            # fall back to the first caption track
            chosen = yt.captions[tracks[0]]
        xml = chosen.xml_captions
        # Very light XML parsing (avoid extra deps)
        import re
        entries = re.findall(r'<text start="([0-9\.]+)" dur="([0-9\.]+)">(.*?)</text>', xml)
        def html_unescape(s: str) -> str:
            import html
            return html.unescape(s.replace("\n", " ").strip())
        return [(float(s), float(d), html_unescape(t)) for s, d, t in entries]
    except Exception:
        return []

def get_video_title(url: str) -> Optional[str]:
    try:
        yt = YouTube(url)
        return yt.title
    except Exception:
        return None
