import os
from pathlib import Path
from unittest.mock import patch

import pytest

from jc.secrets import get_effective_provider, get_llm_api_key, get_llm_model, load_env


def test_get_llm_api_key_prefers_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "openai-123")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("HUGGINGFACE_API_KEY", raising=False)

    # Mock KeyLocker to return None so env takes precedence
    with patch('jc.secrets.KeyLocker.find_key_for_provider', return_value=None):
        assert get_llm_api_key() == "openai-123"


def test_get_llm_api_key_fallbacks_to_openrouter(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key-abc")
    monkeypatch.delenv("HUGGINGFACE_API_KEY", raising=False)

    # Mock KeyLocker to return None so env fallback works
    with patch('jc.secrets.KeyLocker.find_key_for_provider', return_value=None):
        assert get_llm_api_key() == "or-key-abc"


def test_get_llm_api_key_handles_huggingface(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("HUGGINGFACE_API_KEY", "hf-token")

    # Mock KeyLocker to return None so env takes precedence
    with patch('jc.secrets.KeyLocker.find_key_for_provider', return_value=None):
        assert get_llm_api_key() == "hf-token"


def test_get_effective_provider_respects_override(monkeypatch):
    monkeypatch.setenv("JC_PROVIDER", "huggingface")
    monkeypatch.setenv("HUGGINGFACE_API_KEY", "hf-token")

    # Mock KeyLocker to avoid real credentials
    with patch('jc.secrets.KeyLocker.find_key_for_provider', return_value=None):
        assert get_effective_provider() == "huggingface"


def test_get_llm_model_defaults_and_override(monkeypatch):
    monkeypatch.setenv("JC_HUGGINGFACE_MODEL", "custom/model")

    assert get_llm_model("huggingface") == "custom/model"
    assert get_llm_model("openai").startswith("gpt-4o")


def test_load_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=fromfile-xyz\n")

    # Ensure env var not set first
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    load_env(env_file)
    assert os.getenv("OPENAI_API_KEY") == "fromfile-xyz"
