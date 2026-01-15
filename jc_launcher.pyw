#!/usr/bin/env python3
"""Windows-friendly entrypoint for the system tray launcher.

This file intentionally stays very small.
The importable implementation lives in `jc_launcher.py`.
"""

from __future__ import annotations

from jc_launcher import main


if __name__ == "__main__":
    raise SystemExit(main())
