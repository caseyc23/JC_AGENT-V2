#!/usr/bin/env python3
"""Compatibility shim for jc_research.

The maintained implementation lives in the `jc` package.
This file remains so older docs/scripts that reference `jc_research.py` keep working.
"""

from __future__ import annotations

from jc.research import JCResearch, PlatformIntegrations

__all__ = ["JCResearch", "PlatformIntegrations"]


if __name__ == "__main__":
    # Basic smoke test
    r = JCResearch()
    print("jc_research shim loaded; try r.web_search('AI business automation 2025')")
