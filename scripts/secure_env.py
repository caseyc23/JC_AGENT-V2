"""Helpers for loading secrets from secure environment sources."""

from __future__ import annotations

from pathlib import Path
import os
from typing import Iterable

try:
    from dotenv import load_dotenv  # type: ignore[import]
except ImportError:
    load_dotenv = None


def load_env(dotenv_path: Path | str | None = None) -> None:
    """Load a `.env` file if python-dotenv is available."""

    if load_dotenv is None:
        return

    if dotenv_path is None:
        dotenv_path = Path.cwd() / ".env"

    load_dotenv(dotenv_path)


def require_env_var(names: Iterable[str], hint: str | None = None) -> str:
    """Return the first populated environment variable from `names`."""

    load_env()

    for name in names:
        value = os.environ.get(name)
        if value:
            return value

    joined = ", ".join(names)
    message = hint or (
        "Store them securely (env var, CI secret, keychain) before running the script."
    )
    raise EnvironmentError(f"None of {joined} are set. {message}")


def require_secret(
    name: str,
    *,
    aliases: Iterable[str] | None = None,
    hint: str | None = None,
) -> str:
    """Return a named secret, falling back to optional alias environment variables."""

    candidates = [name]
    if aliases:
        candidates.extend(aliases)
    return require_env_var(candidates, hint=hint)


def require_github_token() -> str:
    """Return the GitHub access token from a secure source."""

    return require_secret(
        "GITHUB_TOKEN",
        hint="Set GITHUB_TOKEN via your shell profile, CI secret, or OS keychain before running the script.",
    )


def require_slack_token() -> str:
    """Return the Slack OAuth token from the environment."""

    return require_secret(
        "SLACK_TOKEN",
        aliases=["SLACK_APP_TOKEN"],
        hint="Use your team's secret store or environment variable to populate the Slack token.",
    )


def require_notion_token() -> str:
    """Return the Notion integration token from the environment."""

    return require_secret("NOTION_TOKEN", hint="Provide NOTION_TOKEN securely before running Notion helpers.")


def require_openai_key() -> str:
    """Return the OpenAI API key, preferring OPENAI_API_KEY."""

    return require_secret(
        "OPENAI_API_KEY",
        hint="Store your OpenAI key in OPENAI_API_KEY (or another env var) before starting.",
    )


def require_openrouter_key() -> str:
    """Return the OpenRouter API key as a fallback key pair."""

    return require_secret(
        "OPENROUTER_API_KEY",
        aliases=["OPENROUTER_KEY"],
        hint="OPENROUTER_API_KEY is required for the default provider; set it in a secure store.",
    )


def require_serper_key() -> str:
    """Return the Serper (Search) API key."""

    return require_secret(
        "SERPER_API_KEY",
        hint="SERPER_API_KEY (Serper search) should be provided via env/CI key vault.",
    )


def require_elevenlabs_key() -> str:
    """Return the ElevenLabs API key used for text-to-speech."""

    return require_secret(
        "ELEVENLABS_API_KEY",
        hint="Provide ELEVENLABS_API_KEY securely so speech features can stay local-first.",
    )


def require_huggingface_key() -> str:
    """Return the Hugging Face API key for vector and model access."""

    return require_secret(
        "HUGGINGFACE_API_KEY",
        hint="Set HUGGINGFACE_API_KEY in your environment/CI vault before running Hugging Face flows.",
    )


def require_gmail_credentials() -> str:
    """Return the path/JSON string for Gmail credentials."""

    return require_secret(
        "GMAIL_CREDENTIALS",
        hint="GMAIL_CREDENTIALS points to a JSON file or key string stored securely.",
    )
