#!/usr/bin/env python3
"""Build a simple JSON index from integrations/docs/*.md for jc to query.

Index format: integrations/index.json -> [{"name": <repo>, "path": <docs path>, "content": <text>}]
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "integrations" / "docs"
OUT = ROOT / "integrations" / "index.json"


def build():
    items = []
    if not DOCS.exists():
        print("No docs directory found; run extract_third_party_docs.py first")
        return
    for f in sorted(DOCS.glob("*.md")):
        name = f.stem
        text = f.read_text(encoding="utf-8", errors="ignore")
        # Store a deterministic, portable path (no machine-specific absolute paths).
        items.append({"name": name, "path": f.relative_to(ROOT).as_posix(), "content": text})
    OUT.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote index to {OUT}")


if __name__ == '__main__':
    build()
