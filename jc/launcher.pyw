"""Compatibility wrapper: import original top-level `jc_launcher.pyw` as `jc.launcher`"""
import importlib as _il
_mod = _il.import_module('jc_launcher')
from jc_launcher import *  # noqa: F401,F403
__all__ = [name for name in dir(_mod) if not name.startswith('_')]
