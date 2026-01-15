"""Compatibility wrapper: import original top-level `jc_desktop.py` as `jc.desktop`"""
import importlib as _il
_mod = _il.import_module('jc_desktop')
from jc_desktop import *  # noqa: F401,F403
__all__ = [name for name in dir(_mod) if not name.startswith('_')]
