"""Higher-level search service integrating third-party index and metadata."""
from pathlib import Path
from typing import List, Dict
from .third_party_index import search as _search
from .third_party import list_third_party


ROOT = Path(__file__).resolve().parents[1]


def query_docs(q: str, top: int = 5) -> List[Dict]:
    """Return top search results with a short snippet and repo metadata."""
    results = _search(q)[:top]
    registry = {r['name']: r for r in list_third_party()}
    out = []
    for r in results:
        name = r.get('name')
        path_raw = r.get('path')
        path = Path(path_raw) if path_raw else Path()
        if path_raw and not path.is_absolute():
            path = (ROOT / path).resolve()
        snippet = ''
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
            snippet = text.strip()[:400].replace('\n', ' ')
        except Exception:
            snippet = ''
        meta = registry.get(name, {})
        out.append({
            'name': name,
            'path': str(path),
            'score': r.get('score', 0),
            'snippet': snippet,
            'repo_url': meta.get('url')
        })
    return out
