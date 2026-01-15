from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - dotenv optional at import-time
    load_dotenv = None

from .key_locker import KeyLocker


PROVIDER_FALLBACK_ORDER: Sequence[str] = ["openai", "openrouter", "huggingface"]
PROVIDER_KEY_ENV: dict[str, Sequence[str]] = {
    "openai": ("OPENAI_API_KEY",),
    "openrouter": ("OPENROUTER_API_KEY", "OPENROUTER_KEY"),
    "huggingface": ("HUGGINGFACE_API_KEY",),
}
MODEL_ENV_VARS: dict[str, str] = {
    "openai": "JC_OPENAI_MODEL",
    "openrouter": "JC_OPENROUTER_MODEL",
    "huggingface": "JC_HUGGINGFACE_MODEL",
}
MODEL_DEFAULTS: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "openrouter": "openai/gpt-4o-mini",
    "huggingface": "meta-llama/llama-3.1-8b-instruct",
}


def _normalize_provider(provider: str | None) -> str | None:
    if not provider:
        return None
    normalized = provider.strip().lower()
    if not normalized:
        return None
    return normalized


def _load_env_value(names: Sequence[str]) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def _provider_has_key(provider: str) -> bool:
    if _load_env_value(PROVIDER_KEY_ENV.get(provider, ())):
        return True
    if provider == "huggingface" and _huggingface_key_file():
        return True
    try:
        return KeyLocker.find_key_for_provider(provider) is not None
    except ValueError:
        return False


def load_env(dotenv_path: str | Path | None = None) -> None:
    """Load a local .env file if present.

    This helper is safe to call repeatedly; if python-dotenv isn't
    installed the call is a no-op.
    """
    if dotenv_path is None:
        dotenv_path = Path.cwd() / ".env"
    else:
        dotenv_path = Path(dotenv_path)

    if dotenv_path.exists() and load_dotenv:
        # Do not override already-set environment variables
        load_dotenv(dotenv_path, override=False)


def get_effective_provider() -> str:
    """Return the active provider, honoring `JC_PROVIDER` overrides."""
    override = _normalize_provider(os.getenv("JC_PROVIDER"))
    if override and _provider_has_key(override):
        return override

    for provider in PROVIDER_FALLBACK_ORDER:
        if _provider_has_key(provider):
            return provider

    return "openrouter"


@dataclass
class LLMKeyInfo:
    api_key: str | None
    provider: str | None
    source: str | None
    key_id: str | None


def _huggingface_key_file() -> str | None:
    path = os.getenv("HUGGINGFACE_KEY_FILE")
    if not path:
        return None
    candidate = Path(path)
    if not candidate.exists():
        return None
    try:
        return candidate.read_text(encoding="utf-8").strip()
    except OSError:
        return None


def get_llm_key_info(provider: str | None = None) -> LLMKeyInfo:
    candidate = _normalize_provider(provider)
    order: list[str] = []
    if candidate:
        order.append(candidate)
    order.extend([entry for entry in PROVIDER_FALLBACK_ORDER if entry != candidate])

    for provider_name in order:
        key = _load_env_value(PROVIDER_KEY_ENV.get(provider_name, ()))
        if key:
            return LLMKeyInfo(api_key=key, provider=provider_name, source="env", key_id=None)

        if provider_name == "huggingface":
            file_key = _huggingface_key_file()
            if file_key:
                return LLMKeyInfo(api_key=file_key, provider="huggingface", source="file", key_id=None)

        try:
            locker_entry = KeyLocker.find_key_for_provider(provider_name)
            if locker_entry:
                secret = KeyLocker.get_secret(locker_entry["id"])
                return LLMKeyInfo(
                    api_key=secret,
                    provider=provider_name,
                    source="keylocker",
                    key_id=locker_entry["id"],
                )
        except (KeyError, ValueError):
            continue

    return LLMKeyInfo(api_key=None, provider=None, source=None, key_id=None)


def get_llm_api_key(provider: str | None = None) -> str | None:
    info = get_llm_key_info(provider)
    return info.api_key


def get_llm_model(provider: str | None = None) -> str:
    """Return the preferred model for `provider` or the effective provider."""
    candidate = _normalize_provider(provider)
    if not candidate:
        candidate = get_effective_provider()

    env_var = MODEL_ENV_VARS.get(candidate)
    if env_var:
        override = os.getenv(env_var)
        if override:
            return override

    return MODEL_DEFAULTS.get(candidate, MODEL_DEFAULTS["openrouter"])
