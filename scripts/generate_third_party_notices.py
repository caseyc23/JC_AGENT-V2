#!/usr/bin/env python3
"""Generate a THIRD_PARTY_NOTICES.md from integrations/third_party.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integrations" / "third_party.json"
OUT = ROOT / "THIRD_PARTY_NOTICES.md"


def generate():
    data = json.loads(REGISTRY.read_text())
    lines = ["# Third Party Notices\n"]
    for r in data:
        lines.append(f"## {r['name']}\n")
        lines.append(f"- URL: {r['url']}\n")
        lines.append(f"- Local path: {r['local_path']}\n")
        lines.append(f"- License: {r['license']}\n")
        if r.get('notes'):
            lines.append(f"- Notes: {r['notes']}\n")
        lines.append("\n")
    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")


if __name__ == '__main__':
    generate()
