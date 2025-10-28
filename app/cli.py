
from __future__ import annotations
import argparse, os, sys, pathlib
from dotenv import load_dotenv
from app.llm.providers import LLMConfig
from app.agent import run_agent
from app.utils.slugify import slugify, slug_from_youtube_url
from app.extractors.transcript import get_video_title

def main():
    load_dotenv()
    ap = argparse.ArgumentParser(description="YouTube → Markdown Notes (Extended)")
    ap.add_argument("--url", required=True, help="YouTube URL")
    ap.add_argument("--provider", default=os.getenv("PROVIDER", "openai"), choices=["openai","anthropic"])
    ap.add_argument("--model", default=os.getenv("MODEL", "gpt-4o-mini"))
    ap.add_argument("--max-tokens", type=int, default=1800)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--language", default=None, help="Target language: 'de' or 'en' (default auto)")
    ap.add_argument("--quotes", type=int, default=5, help="Number of timestamped quotes to include")
    args = ap.parse_args()

    cfg = LLMConfig(
        provider=args.provider,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        language=args.language,
        quotes=args.quotes,
    )

    md, title = run_agent(args.url, cfg)

    # Slug logic: prefer video title; fall back to id/path
    if title:
        slug = slugify(title)
    else:
        slug = slug_from_youtube_url(args.url)

    out_dir = pathlib.Path("output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"
    out_path.write_text(md, encoding="utf-8")

    print(f"\nSaved: {out_path.resolve()}")

if __name__ == "__main__":
    main()
