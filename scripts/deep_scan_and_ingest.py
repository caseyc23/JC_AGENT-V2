#!/usr/bin/env python3
"""
Recursively scan given root paths for potential API keys and register them into KeyLocker (preferred)
or the raw keyring service `jc-agent`.

Usage:
  python scripts/deep_scan_and_ingest.py <root1> <root2> ...

Notes:
 - This script is conservative: it scans common file extensions, skips very large files,
   and never prints secret values. Only prints presence status for stored keys.
 - It attempts to register keys with `jc.key_locker.KeyLocker` when available.

"""
from __future__ import annotations

import sys
import os
import re
from pathlib import Path
from typing import Dict, List

# Heuristics copied from ingest_keys_from_files.py
EXPLICIT_PATTERNS = {
    "OPENAI_API_KEY": re.compile(r"(?:OPENAI_API_KEY|\$env:OPENAI_API_KEY)\s*[:=]\s*['\"]?([A-Za-z0-9\-_.]+)['\"]?", re.IGNORECASE),
    "GEMINI_API_KEY": re.compile(r"(?:GEMINI_API_KEY|\$env:GEMINI_API_KEY)\s*[:=]\s*['\"]?([A-Za-z0-9\-_.]+)['\"]?", re.IGNORECASE),
    "FRED_API_KEY": re.compile(r"(?:FRED_API_KEY)\s*[:=]\s*['\"]?([A-Za-z0-9\-_.]+)['\"]?", re.IGNORECASE),
    "GITHUB_TOKEN": re.compile(r"(?:GITHUB_TOKEN|\$env:GITHUB_TOKEN)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]+)['\"]?", re.IGNORECASE),
    "HUGGINGFACE_API_KEY": re.compile(r"(?:HUGGINGFACE_API_KEY)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]+)['\"]?", re.IGNORECASE),
    "OPENROUTER_API_KEY": re.compile(r"(?:OPENROUTER_API_KEY|\$env:OPENROUTER_API_KEY)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]+)['\"]?", re.IGNORECASE),
    "JC_SECRETS_PASSPHRASE": re.compile(r"(?:JC_SECRETS_PASSPHRASE)\s*[:=]\s*['\"]?(.+?)['\"]?", re.IGNORECASE),
}

PREFIX_PATTERNS = {
    "OPENAI_API_KEY": re.compile(r"(sk-[A-Za-z0-9\-_.]{10,})"),
    "GEMINI_API_KEY": re.compile(r"(ya29\.[A-Za-z0-9_\-\.]+|AIza[A-Za-z0-9_\-]+)"),
    "GITHUB_TOKEN": re.compile(r"(gh[opusr]_[A-Za-z0-9_\-]+)"),
    "HUGGINGFACE_API_KEY": re.compile(r"(hf_[A-Za-z0-9_\-]+)"),
    "OPENROUTER_API_KEY": re.compile(r"(orsk-or-[A-Za-z0-9_\-]+|or-[A-Za-z0-9_\-]+)"),
}

# File extensions we'll consider
CANDIDATE_EXTS = {
    ".env",
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".sh",
    ".ps1",
    ".bat",
    ".ini",
    ".cfg",
    ".ipynb",
    ".js",
    ".ts",
    ".html",
    ".css",
}

# Skip files larger than this (bytes)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def read_file_text(path: Path) -> str:
    # Read only the first chunk of the file to avoid blocking on very large
    # or special files (e.g., device files). This is sufficient for finding
    # API keys which are typically near the start of files.
    MAX_READ_BYTES = 256 * 1024  # 256 KB
    try:
        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                return ""
        except Exception:
            # If stat fails, continue and attempt a guarded read
            pass
        with path.open("rb") as fh:
            data = fh.read(MAX_READ_BYTES)
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    except Exception:
        return ""


def extract_from_text(text: str) -> Dict[str, str]:
    found: Dict[str, str] = {}

    for name, pat in EXPLICIT_PATTERNS.items():
        m = pat.search(text)
        if m:
            found[name] = m.group(1).strip()

    for name, pat in PREFIX_PATTERNS.items():
        if name in found:
            continue
        m = pat.search(text)
        if m:
            found[name] = m.group(1).strip()

    return found


def gather_candidate_files(root: Path, max_depth: int | None = None) -> List[Path]:
    files: List[Path] = []
    if root.is_file():
        files.append(root)
        return files
    try:
        if max_depth is None:
            iterator = root.rglob("*")
        else:
            # Custom recursive walk with depth limit
            def walk_limited(p: Path, depth: int):
                if depth < 0:
                    return
                try:
                    for child in p.iterdir():
                        yield child
                        if child.is_dir():
                            yield from walk_limited(child, depth - 1)
                except Exception:
                    return

            iterator = walk_limited(root, max_depth)

        for path in iterator:
            try:
                if not path.is_file():
                    continue
                if path.suffix.lower() in CANDIDATE_EXTS:
                    files.append(path)
            except Exception:
                continue
    except Exception:
        # In case of permission errors or very large trees
        pass
    return files


def main(args: List[str]) -> int:
    if not args:
        print("Provide one or more root directories to scan (e.g., Desktop, OneDrive)")
        return 2

    # Allow optional --max-depth=N argument
    max_depth: int | None = None
    filtered_args: List[str] = []
    for a in args:
        if a.startswith("--max-depth="):
            try:
                max_depth = int(a.split("=", 1)[1])
            except Exception:
                max_depth = None
        else:
            filtered_args.append(a)

    aggregate_found: Dict[str, str] = {}

    roots = [Path(a) for a in filtered_args]

    for root in roots:
        if not root.exists():
            print(f"Skipping non-existent path: {root}")
            continue
        print(f"Scanning: {root}")
        candidates = gather_candidate_files(root, max_depth=max_depth)
        print(f"  candidate files found: {len(candidates)}")
        for f in candidates:
            text = read_file_text(f)
            if not text:
                continue
            found = extract_from_text(text)
            for k, v in found.items():
                if k not in aggregate_found:
                    aggregate_found[k] = v

    if not aggregate_found:
        print("No keys discovered in scanned locations.")
        return 0

    # Store discovered keys
    stored: Dict[str, bool] = {}
    try:
        from jc.key_locker import KeyLocker
        have_keylocker = True
    except Exception:
        KeyLocker = None  # type: ignore
        have_keylocker = False

    try:
        import keyring as _kr
    except Exception:
        _kr = None

    provider_map = {
        "OPENAI_API_KEY": "openai",
        "OPENROUTER_API_KEY": "openrouter",
        "HUGGINGFACE_API_KEY": "huggingface",
        "GEMINI_API_KEY": "gemini",
        "GITHUB_TOKEN": "github",
        "FRED_API_KEY": "fred",
        "JC_SECRETS_PASSPHRASE": "secrets",
    }

    service = "jc-agent"

    for k, v in aggregate_found.items():
        if have_keylocker and KeyLocker is not None:
            try:
                existing = None
                try:
                    existing = KeyLocker.find_key_for_provider(provider_map.get(k, k.lower()))
                except Exception:
                    existing = None
                KeyLocker.add_key(name=k, provider=provider_map.get(k, k.lower()), secret=v)
                stored[k] = True
                if _kr:
                    try:
                        _kr.delete_password(service, k)
                    except Exception:
                        pass
            except Exception:
                stored[k] = False
        else:
            if _kr:
                try:
                    _kr.set_password(service, k, v)
                    stored[k] = True
                except Exception:
                    stored[k] = False
            else:
                stored[k] = False

    for k, s in stored.items():
        print(f"STORED {k}: {s}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
