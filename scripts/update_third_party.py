#!/usr/bin/env python3
"""
Simple updater for third-party repos listed in integrations/third_party.json.
It will git clone missing repos and git pull existing ones.
"""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integrations" / "third_party.json"


def run(cmd, cwd=None):
    print(f"> {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def update():
    data = json.loads(REGISTRY.read_text())
    for repo in data:
        path = ROOT / repo["local_path"]
        url = repo["url"]
        if path.exists():
            try:
                run(f"git -C {path} fetch --all --prune")
                run(f"git -C {path} pull --ff-only")
            except Exception as e:
                print(f"Warning: failed to update {repo['name']}: {e}")
        else:
            try:
                run(f"git clone {url} {path}")
            except Exception as e:
                print(f"Warning: failed to clone {repo['name']}: {e}")


if __name__ == "__main__":
    update()
