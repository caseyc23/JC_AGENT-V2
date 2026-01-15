import subprocess
import sys
from jc.search_service import query_docs


def test_query_docs_build_index():
    # Ensure index exists by running extractor and builder
    subprocess.check_call([sys.executable, "scripts/extract_third_party_docs.py"])
    subprocess.check_call([sys.executable, "scripts/build_third_party_index.py"])
    res = query_docs("index", top=3)
    assert isinstance(res, list)
