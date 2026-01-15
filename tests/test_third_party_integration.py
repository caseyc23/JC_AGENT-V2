import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "integrations" / "docs"
INDEX = ROOT / "integrations" / "index.json"


def test_extract_and_build():
    # Run extractor and builder
    subprocess.check_call([sys.executable, "scripts/extract_third_party_docs.py"])
    subprocess.check_call([sys.executable, "scripts/build_third_party_index.py"])
    assert INDEX.exists()
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    assert isinstance(data, list)


def test_cli_query():
    # Ensure query CLI runs and returns text
    p = subprocess.run([sys.executable, "scripts/query_third_party.py", "index", "--top", "3"], capture_output=True, text=True)
    assert p.returncode == 0
    assert "No results found" not in p.stdout
