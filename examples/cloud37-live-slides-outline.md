# Cloud37 Recruiting-Case – Live-Session (3 Slides)

## Slide 1 — Use Case & USP
- **Problem**: YouTube ist reich an Wissen, aber zeitintensiv und inkonsistent.
- **Lösung**: CLI-Agent wandelt 2–5‑min Videos in **konsistente, teilbare Markdown‑Notizen** um.
- **USP**: Einfache Bedienung (CLI), klare Struktur (TL;DR, Kernaussagen, Outline, Zitate), Provider‑agnostisch (OpenAI/Anthropic), reproduzierbar.

## Slide 2 — Architekturüberblick
- **Flow**: URL → Transcript‑Fetcher (YTA / PyTube Fallback) → LLM‑Provider → Markdown‑Formatter → `output/<slug>.md`
- **Kernmodule**: `extractors/transcript.py`, `llm/providers.py`, `md/formatter.py`, `agent.py`, `cli.py`
- **Design‑Entscheidungen**: geringe Temperatur, erweiterte Sektionen, saubere Trennung der Verantwortlichkeiten.
- **Grenzen**: keine Captions ⇒ Abbruch; Zitat‑Genauigkeit ∝ Transcript‑Qualität; potenzielle Halluzinationen ⇒ konservative Prompts.

## Slide 3 — Demo & Ergebnis
- **Input**: `--url https://www.youtube.com/watch?v=wCEgUfWVLrI`
- **Output**: `output/what-is-overfitting-wCEgUfWVLrI.md` (extended)
- **Highlight**: 3–5 TL;DR‑Bullets, prägnante Kernaussagen, 5 Zitate mit Zeitstempel, Glossar & offene Fragen.
- **Next Steps**: optionales Caching, Batch‑Mode, Quellzitate‑Validierung, RAG‑Ablage für teamweite Suche.