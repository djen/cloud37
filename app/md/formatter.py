
from __future__ import annotations
import re

def ensure_extended_sections(md: str) -> str:
    """Guarantee that extended sections exist; add empty stubs if missing."""
    required = [
        "## TL;DR",
        "## Kernaussagen",
        "## Struktur / Outline",
        "## Zitate mit Zeitstempel",
        "## Glossar",
        "## Offene Fragen",
        "## Weiterführende Links",
    ]
    for sec in required:
        if sec not in md:
            md += f"\n\n{sec}\n- —"
    return md

def normalize_timestamps(md: str) -> str:
    """Normalize timestamps to [mm:ss] where possible."""
    def fix(match):
        t = match.group(1)
        # t can be float seconds or 'mm:ss'
        try:
            if ":" in t:
                mm, ss = t.split(":")
                return f"[{int(mm):02d}:{int(ss):02d}]"
            else:
                secs = float(t)
                mm = int(secs // 60)
                ss = int(round(secs % 60))
                return f"[{mm:02d}:{ss:02d}]"
        except Exception:
            return f"[{t}]"
    return re.sub(r"\[(\d+(?::\d+)?)\]", fix, md)
