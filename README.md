
# Cloud37 Recruiting Case – YouTube → Markdown Notes Agent (Python CLI)

> Extracts the essence of a **2–5 min public YouTube video** into a **structured Markdown note**: TL;DR, key takeaways, outline — plus **extended sections** (quotes with timestamps, glossary, open questions, further links).  
> Stack: **Python**, `youtube-transcript-api`, OpenAI/Anthropic (pluggable).  
> Output: `output/<slug>.md`

---

## 1) Quick Start

```bash
# Python 3.10+ recommended
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# add your OPENAI_API_KEY and/or ANTHROPIC_API_KEY

# Run
python -m app.cli --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"   --provider openai   --model gpt-4o-mini
```

Output file will be written to `output/<slug>.md`.

---

## 2) What it does (Pipeline)

1. **Fetch transcript** via `youtube-transcript-api` (tries auto-generated and manual tracks).  
   Fallback: try caption tracks via `pytube`.  
   If no transcript is available, the tool will stop with a clear message.
2. **Summarize & structure** using your chosen LLM (OpenAI or Anthropic).  
   We use concise prompts to generate: TL;DR, key takeaways, outline, quotes with timestamps, glossary, open questions, further links.
3. **Generate Markdown** in the required structure and save to `output/<slug>.md`.

---

## 3) CLI Options

```bash
python -m app.cli --help
```

Key flags:
- `--url` YouTube URL (required)
- `--provider` `openai` or `anthropic` (default from `.env`)
- `--model` model name (e.g. `gpt-4o-mini`, `gpt-4.1-mini`, `claude-3-5-sonnet-latest`)
- `--max-tokens` response cap (default 1800)
- `--temperature` 0.2 by default
- `--language` target note language (`de` or `en`, default: auto; falls back to English)
- `--quotes` number of timestamped quotes (default 5)

---

## 4) Output Format (Extended)

```markdown
# <Videotitel>
- Quelle: <YouTube-URL>

## TL;DR (3–5 Bullet Points)
- ...

## Kernaussagen
- ...
- ...

## Struktur / Outline
1. ...
2. ...

## Zitate mit Zeitstempel
- [00:42] „...“
- [01:55] „...“

## Glossar (Begriffe → Kurzdefinition)
- Begriff: Erklärung

## Offene Fragen / Weiteres Nachforschen
- ...

## Weiterführende Links
- ...
```

---

## 5) Notes & Design Decisions

- **No frontend** — per brief, a simple CLI is sufficient.
- **Deterministic-ish**: default `temperature=0.2` for crisp notes.
- **Separation of concerns**: transcript fetchers, LLM providers, and markdown formatting are modular.
- **Slug**: derived from video title or URL; ensures stable file name.

---

## 6) Repository Layout

```
app/
  cli.py                  # argparse entrypoint
  agent.py                # orchestration
  extractors/transcript.py
  llm/providers.py
  md/formatter.py
  utils/slugify.py
output/
examples/
```

---

## 7) License

Provided solely for the Cloud37 recruiting process
