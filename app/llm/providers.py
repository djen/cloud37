
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LLMConfig:
    provider: str = os.getenv("PROVIDER", "openai")
    model: str = os.getenv("MODEL", "gpt-4o-mini")
    temperature: float = 0.2
    max_tokens: int = 1800
    language: Optional[str] = None  # 'de' or 'en'
    quotes: int = 5

SYSTEM_PROMPT = """You are an expert note-taker creating crisp, factual, structured Markdown notes from short YouTube transcripts.
Always produce valid Markdown. Avoid hallucinations. If information is missing, leave placeholders like '—'."""

def build_user_prompt(video_title: str, url: str, transcript: str, cfg: LLMConfig) -> str:
    lang = cfg.language or "auto"
    return f"""Create an **extended** structured Markdown note for the YouTube video below.
Target language: {lang} (if 'auto', infer from transcript, else use exactly this language).

Use this exact structure:

# <Videotitel>
- Quelle: {url}

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

Constraints:
- Brief, high-signal bullets. Avoid repetition.
- Use **verbatim** quotes only from provided transcript.
- Include up to {cfg.quotes} quotes with [mm:ss] timestamps when identifiable from transcript snippets.
- If the video title is known, place it in <Videotitel>. Otherwise, infer a short, accurate title.
- If transcript language is German, use German section headings as shown; otherwise translate headings appropriately.

Video title (may be empty): {video_title}

Transcript (verbatim):

{transcript}
"""

class LLMProvider:
    def __init__(self, cfg: LLMConfig):
        self.cfg = cfg

    def complete(self, video_title: str, url: str, transcript: str) -> str:
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    def __init__(self, cfg: LLMConfig):
        super().__init__(cfg)
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def complete(self, video_title: str, url: str, transcript: str) -> str:
        prompt = build_user_prompt(video_title, url, transcript, self.cfg)
        resp = self.client.chat.completions.create(
            model=self.cfg.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=self.cfg.temperature,
            max_tokens=self.cfg.max_tokens,
        )
        return resp.choices[0].message.content.strip()

class AnthropicProvider(LLMProvider):
    def __init__(self, cfg: LLMConfig):
        super().__init__(cfg)
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def complete(self, video_title: str, url: str, transcript: str) -> str:
        prompt = build_user_prompt(video_title, url, transcript, self.cfg)
        msg = self.client.messages.create(
            model=self.cfg.model,
            max_tokens=self.cfg.max_tokens,
            temperature=self.cfg.temperature,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        # New SDK returns content list
        parts = []
        for p in msg.content:
            if getattr(p, "type", None) == "text":
                parts.append(p.text)
        return "\n".join(parts).strip()

def get_provider(cfg: LLMConfig) -> LLMProvider:
    p = (cfg.provider or "openai").lower()
    if p == "anthropic":
        return AnthropicProvider(cfg)
    return OpenAIProvider(cfg)
