
# Cloud37 Recruiting Case – YouTube → Markdown Notes Agent (Python CLI)

Extracts a **2–5 min public YouTube video** into a **structured Markdown note**: TL;DR, key takeaways, outline — plus **extended sections** (quotes with timestamps, glossary, open questions, further links).  
Stack: **Python**, `youtube-transcript-api` v1.x, OpenAI/Anthropic.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# add your API keys
python -m app.cli --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --provider openai --model gpt-4o-mini
```

Output → `output/<slug>.md`

## Pipeline
1) Fetch transcript via `youtube-transcript-api` v1.x `.fetch()` (fallback: `pytube` captions).  
2) Summarize with your LLM provider.  
3) Generate extended Markdown.

## CLI flags
See `python -m app.cli --help`.

- `--url` (required)  
- `--provider` `openai|anthropic`  
- `--model` (e.g. `gpt-4o-mini` / `claude-3-5-sonnet-latest`)  
- `--language` `de|en` (default: auto)  
- `--quotes` number of timestamped quotes (default 5)

## Output (Extended)
```markdown
# <Videotitel>
- Quelle: <YouTube-URL>

## TL;DR (3–5 Bullet Points)
- ...

## Kernaussagen
- ...

## Struktur / Outline
1. ...

## Zitate mit Zeitstempel
- [mm:ss] "…"

## Glossar (Begriffe → Kurzdefinition)
- Begriff: Erklärung

## Offene Fragen / Weiteres Nachforschen
- ...

## Weiterführende Links
- ...
```

---

### Note on `youtube-transcript-api` v1.x

This repo uses the **new v1.x interface**:

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
fetched = ytt_api.fetch(video_id, languages=['de','en'])
# ... or list available:
tlist = ytt_api.list(video_id)
```
