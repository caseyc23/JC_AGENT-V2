"""Workspace indexer utilities for JC.

Provides a small indexer that walks a workspace directory, collects file
metadata (path, size, language hint, snippet) and computes simple summaries.
This is intentionally lightweight and avoids heavy dependencies.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List


EXT_LANG_MAP = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".md": "Markdown",
    ".json": "JSON",
    ".html": "HTML",
    ".css": "CSS",
    ".java": "Java",
    ".rb": "Ruby",
    ".go": "Go",
}


def _guess_language(filename: str, content: str | None) -> str:
    ext = Path(filename).suffix.lower()
    if ext in EXT_LANG_MAP:
        return EXT_LANG_MAP[ext]
    if content:
        if "import " in content and " from " in content:
            return "TypeScript/JavaScript"
        if "def " in content and "import " in content:
            return "Python"
    return "text"


def _read_snippet(path: Path, max_chars: int = 800) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        return text[:max_chars]
    except Exception:
        return ""


def index_workspace(workspace_dir: str | Path) -> Dict[str, object]:
    ws = Path(workspace_dir)
    files: List[Dict[str, object]] = []

    def walk(dir_path: Path) -> None:
        for entry in dir_path.iterdir():
            try:
                if entry.is_dir():
                    if entry.name in (".git", "node_modules"):
                        continue
                    walk(entry)
                else:
                    size = entry.stat().st_size
                    snippet = _read_snippet(entry, max_chars=1000)
                    lang = _guess_language(entry.name, snippet)
                    rel = str(entry.relative_to(ws))
                    files.append({"path": rel, "size": size, "lang": lang, "snippet": snippet[:800]})
            except Exception:
                # Best-effort: skip unreadable files
                continue

    if not ws.exists():
        return {"workspaceDir": str(ws), "fileCount": 0, "topLanguages": [], "files": []}

    walk(ws)

    # Summarize languages
    lang_count: dict[str, int] = {}
    for f in files:
        lang = f.get("lang") or "unknown"
        lang_count[lang] = lang_count.get(lang, 0) + 1

    top_langs = [{"lang": k, "count": v} for k, v in sorted(lang_count.items(), key=lambda x: x[1], reverse=True)[:10]]

    metadata = {
        "workspaceDir": str(ws),
        "fileCount": len(files),
        "topLanguages": top_langs,
        "files": files[:200],
    }
    return metadata


def folder_size(folder: str | Path) -> int:
    p = Path(folder)
    total = 0
    if not p.exists():
        return 0
    for root, dirs, filenames in os.walk(p):
        for f in filenames:
            try:
                total += (Path(root) / f).stat().st_size
            except Exception:
                continue
    return total


__all__ = ["index_workspace", "folder_size"]
