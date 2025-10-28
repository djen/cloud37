
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple
from app.extractors.transcript import yt_video_id, fetch_transcript_yta, fetch_transcript_pytube, get_video_title
from app.llm.providers import LLMConfig, get_provider
from app.md.formatter import ensure_extended_sections, normalize_timestamps

@dataclass
class TranscriptResult:
    segments: List[Tuple[float, float, str]]  # (start, duration, text)
    joined_text: str

def get_transcript(url: str, languages: Optional[List[str]] = None) -> TranscriptResult:
    vid = yt_video_id(url)
    segs = fetch_transcript_yta(vid, languages=languages)
    if not segs:
        segs = fetch_transcript_pytube(url, lang_priority=languages)
    if not segs:
        raise RuntimeError("No transcript or captions available for this video.")
    # Join with lightweight timestamps markers like [start]
    joined = []
    for (start, dur, text) in segs:
        mm = int(start // 60)
        ss = int(round(start % 60))
        joined.append(f"[{mm:02d}:{ss:02d}] {text}")
    return TranscriptResult(segments=segs, joined_text="\n".join(joined))

def run_agent(url: str, cfg: LLMConfig) -> str:
    title = get_video_title(url) or ""
    tr = get_transcript(url, languages=["de", "en"])
    provider = get_provider(cfg)
    md = provider.complete(title, url, tr.joined_text)
    md = ensure_extended_sections(md)
    md = normalize_timestamps(md)
    return md, title
