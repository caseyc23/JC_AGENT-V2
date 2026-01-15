"""Compatibility wrapper for JC's FastAPI app.

Historically this module re-exported symbols from the top-level `agent_api.py`.
The canonical API entrypoint is now `jc_agent_api.py`.
"""

import importlib as _il

_mod = _il.import_module("jc_agent_api")
from jc_agent_api import *  # noqa: F401,F403

__all__ = [name for name in dir(_mod) if not name.startswith("_")]
