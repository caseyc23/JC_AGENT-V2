#!/usr/bin/env python3
"""Compatibility shim for jc_voice
Delegates to `jc.voice` and re-exports main classes/functions.
"""

from jc.voice import JCVoice, VoiceCommands

__all__ = ["JCVoice", "VoiceCommands"]

if __name__ == "__main__":
	# Basic smoke test when executed directly
	v = JCVoice(use_elevenlabs=False)
	v.speak("JC voice shim loaded", wait=True)
