"""
JC-Agent Guardrails Module

This module provides a simple guardrails system to filter, rephrase, or block unsafe or undesired outputs from the agent.
"""

from typing import Callable, List
import re

class Guardrail:
    def __init__(self, name: str, check: Callable[[str], bool], action: Callable[[str], str]):
        self.name = name
        self.check = check
        self.action = action

    def apply(self, text: str) -> str:
        if self.check(text):
            return self.action(text)
        return text

class GuardrailsManager:
    def __init__(self, guardrails: List[Guardrail] = None):
        self.guardrails = guardrails or []

    def add_guardrail(self, guardrail: Guardrail):
        self.guardrails.append(guardrail)

    def apply(self, text: str) -> str:
        for guardrail in self.guardrails:
            text = guardrail.apply(text)
        return text

# Example guardrails
# Block outputs containing banned words
BANNED_WORDS = ["password", "credit card", "ssn"]
def block_banned_words(text: str) -> bool:
    return any(word in text.lower() for word in BANNED_WORDS)
def block_action(text: str) -> str:
    return "[Output blocked due to policy violation.]"

# Rephrase outputs that are too long
def too_long(text: str) -> bool:
    return len(text) > 500
def rephrase_action(text: str) -> str:
    return text[:500] + "... [truncated]"

# Usage example:
# guardrails = GuardrailsManager([
#     Guardrail("BlockBannedWords", block_banned_words, block_action),
#     Guardrail("TruncateLong", too_long, rephrase_action)
# ])
# safe_output = guardrails.apply(agent_output)
