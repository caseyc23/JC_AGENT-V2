#!/usr/bin/env python3
"""Compatibility shim for jc_settings_gui.
This module re-exports helper functions from `jc.settings_gui` so older
imports like `from jc_settings_gui import write_env_atomic` continue to work.
"""

from pathlib import Path
import importlib.util

# Load jc/settings_gui.py directly to avoid importing the `jc` package
# (the package __init__ may have heavy side-effects during import).
_path = Path(__file__).parent / "jc" / "settings_gui.py"
_spec = importlib.util.spec_from_file_location("jc_settings_gui_impl", str(_path))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

write_env_atomic = _mod.write_env_atomic
is_valid_port = _mod.is_valid_port
read_env_file = _mod.read_env_file

__all__ = ["write_env_atomic", "is_valid_port", "read_env_file"]
