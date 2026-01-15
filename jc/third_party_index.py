"""Runtime index access for third-party docs.

Provides a tiny search() that does substring matching against the built index.
"""
import json
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "integrations" / "index.json"


def load_index():
    try:
        return json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception:
        return []


def search(q: str) -> List[dict]:
    q = q.lower().strip()
    results = []
    for item in load_index():
        cnt = item.get("content", "").lower().count(q)
        if cnt > 0:
            path_raw = item.get("path")
            p = Path(path_raw) if path_raw else Path()
            if path_raw and not p.is_absolute():
                p = (ROOT / p).resolve()
            results.append({"name": item.get("name"), "path": str(p) if path_raw else "", "score": cnt})
    return sorted(results, key=lambda x: x["score"], reverse=True)
