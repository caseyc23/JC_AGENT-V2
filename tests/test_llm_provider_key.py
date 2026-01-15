from jc.llm_provider import LLMProvider


def test_llm_provider_uses_openrouter_key(monkeypatch):
    # Ensure open router is picked when OpenAI is absent
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key-abc")
    monkeypatch.delenv("HUGGINGFACE_API_KEY", raising=False)

    provider = LLMProvider()
    assert provider.provider == "openrouter"
    assert provider.api_key == "or-key-abc"


def test_llm_provider_uses_huggingface_when_requested(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("HUGGINGFACE_API_KEY", "hf-key")
    monkeypatch.setenv("JC_PROVIDER", "huggingface")

    provider = LLMProvider()
    assert provider.provider == "huggingface"
    assert provider.api_key == "hf-key"
