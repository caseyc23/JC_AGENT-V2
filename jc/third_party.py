"""Runtime helpers for accessing third-party metadata."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integrations" / "third_party.json"


def list_third_party():
    try:
        return json.loads(REGISTRY.read_text())
    except Exception:
        return []


def find_by_name(name):
    for r in list_third_party():
        if r.get("name") == name:
            return r
    return None
