#!/usr/bin/env python3
"""Query the third-party docs index and print top results.

Usage: python3 scripts/query_third_party.py "search terms" --top 5
"""
import argparse
import sys
from pathlib import Path

# Ensure project root is on sys.path for subprocess/CLI usage
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jc.third_party_index import search


def main():
    p = argparse.ArgumentParser(description="Query third-party docs index")
    p.add_argument("q", help="Query string")
    p.add_argument("--top", type=int, default=5, help="Number of results to show")
    args = p.parse_args()

    results = search(args.q)[: args.top]
    if not results:
        print("No results found")
        return
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['name']} (score={r['score']})\n   path: {r['path']}")


if __name__ == '__main__':
    main()
