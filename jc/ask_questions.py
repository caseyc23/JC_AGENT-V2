"""Ask-questions helper: build prompt from workspace metadata and call LLM with mock fallback.

This module provides a small, focused API used by the HTTP endpoint to generate a
prioritized list of short clarifying questions for a workspace. If no LLM key is
available the module returns a deterministic mock list so the UI and flows can be
exercised without external keys.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

from .llm_provider import LLMProvider


def build_ask_questions_prompt(meta: Dict[str, Any]) -> str:
    readme = (meta.get("README") or "").strip()
    readme_snip = readme[:1200]
    top_files = meta.get("top_files") or []
    top_files_text = "\n".join(f"- {f}" for f in top_files[:10])
    langs = meta.get("top_languages") or []
    if langs and isinstance(langs[0], dict):
        langs_text = ", ".join(f"{l.get('lang')}({l.get('count')})" for l in langs[:10])
    else:
        langs_text = ", ".join(str(l) for l in langs[:10])
    commits = "\n".join((meta.get("recent_commits") or [])[:6])

    parts = [
        "Workspace metadata:",
        f"WorkspaceId: {meta.get('workspaceId')}",
    ]
    if readme_snip:
        parts.append(f"README (snippet):\n{readme_snip}")
    if top_files_text:
        parts.append(f"Top files:\n{top_files_text}")
    if langs_text:
        parts.append(f"Top languages: {langs_text}")
    if commits:
        parts.append(f"Recent commits:\n{commits}")

    parts.extend([
        "",
        "Instruction:",
        (
            "You are JC, a developer assistant. Based on the workspace metadata above, produce a prioritized"
            " list of 6–10 short, one-line clarifying questions that will unblock development fastest."
            " Prefer questions about the project's primary goal, critical files, secrets/configs, deployment"
            " target, tests, and priorities. Number the questions (1., 2., ...). Be concise."
        ),
    ])

    return "\n\n".join(parts)


def parse_questions_from_text(text: str) -> List[str]:
    if not text:
        return []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    questions: List[str] = []
    for l in lines:
        m = re.match(r"^\d+[\.\)]\s*(.+)$", l)
        if m:
            questions.append(m.group(1).strip())
    if not questions:
        # Fallback: treat the first short lines as questions
        for l in lines:
            if len(l) < 240:
                questions.append(l)
            if len(questions) >= 8:
                break
    return questions[:10]


def mock_questions() -> List[str]:
    return [
        "What's the primary goal for this project in one sentence?",
        "Which files or directories should never be modified automatically?",
        "Are there any required env vars or API keys needed to run the project locally?",
        "Which deployment target do you prefer (Vercel, Replit, self-host)?",
        "Are there unit or integration tests we should run automatically on each PR?",
        "What are the top three priorities you'd like JC to focus on first?",
    ]


def generate_clarifying_questions(meta: Dict[str, Any]) -> List[str]:
    """Return a list of clarifying questions for the provided workspace metadata.

    The function will attempt to call the configured LLM provider via
    `LLMProvider`. If there is no available key or the LLM call fails, a
    deterministic mock list is returned so the flow remains testable offline.
    """
    prompt = build_ask_questions_prompt(meta)
    messages = [{"role": "user", "content": prompt}]

    try:
        llm = LLMProvider()
        # Use the provider; LLMProvider will raise if no key is present.
        resp = llm.call(messages, stream=False)
        questions = parse_questions_from_text(resp)
        if questions:
            return questions
    except Exception:
        # Fall through to mock on any error (no key, unreachable API, etc.)
        pass

    return mock_questions()


__all__ = [
    "generate_clarifying_questions",
    "build_ask_questions_prompt",
    "parse_questions_from_text",
]
