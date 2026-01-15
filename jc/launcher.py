"""Importable compatibility wrapper for the system tray launcher.

Historically the repo shipped a top-level `jc_launcher.pyw`, which is not importable
via Python's module system. The importable implementation now lives in
`jc_launcher.py`.

This module keeps `import jc.launcher` working.
"""

from __future__ import annotations

import importlib as _il

_mod = _il.import_module("jc_launcher")
from jc_launcher import *  # noqa: F401,F403

__all__ = [name for name in dir(_mod) if not name.startswith("_")]
