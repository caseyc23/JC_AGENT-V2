"""Compatibility wrapper: import original top-level `jc_self_awareness.py` as `jc.self_awareness`"""
import importlib as _il
_mod = _il.import_module('jc_self_awareness')
from jc_self_awareness import *  # noqa: F401,F403
__all__ = [name for name in dir(_mod) if not name.startswith('_')]
