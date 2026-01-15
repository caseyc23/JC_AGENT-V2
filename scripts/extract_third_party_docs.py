#!/usr/bin/env python3
"""Extract README/docs from third-party repos into integrations/docs/ for indexing.

For each repo in integrations/third_party.json, this copies README.* and any files
in a top-level `docs/` directory into `integrations/docs/<repo>.md`.
"""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integrations" / "third_party.json"
OUT_DIR = ROOT / "integrations" / "docs"


def gather_readme(repo_path: Path) -> str | None:
    # Look for common README filenames
    for name in ("README.md", "README.MD", "README", "readme.md"):
        p = repo_path / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="ignore")
    return None


def gather_docs_dir(repo_path: Path) -> str | None:
    docs_dir = repo_path / "docs"
    if docs_dir.exists() and docs_dir.is_dir():
        parts = []
        for f in sorted(docs_dir.rglob("*.md")):
            parts.append("# " + str(f.relative_to(repo_path)))
            parts.append(f.read_text(encoding="utf-8", errors="ignore"))
        return "\n\n".join(parts)
    return None


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for r in data:
        repo_path = ROOT / r["local_path"]
        out_file = OUT_DIR / f"{r['name']}.md"
        contents = []
        if not repo_path.exists():
            print(f"Skipping {r['name']}: path {repo_path} not found")
            continue
        readme = gather_readme(repo_path)
        if readme:
            contents.append(readme)
        docs = gather_docs_dir(repo_path)
        if docs:
            contents.append(docs)
        if contents:
            out_file.write_text("\n\n---\n\n".join(contents), encoding="utf-8")
            print(f"Wrote {out_file}")
        else:
            print(f"No docs found for {r['name']}")


if __name__ == '__main__':
    main()
