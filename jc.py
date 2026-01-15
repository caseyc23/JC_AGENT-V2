#!/usr/bin/env python3
"""Backwards-compatible entry point.

The canonical entrypoint is the `jc` package (run with `python -m jc`).
This shim exists for older scripts/tools that still call `python jc.py`.
"""

import asyncio

from jc import main


if __name__ == "__main__":
    asyncio.run(main())
