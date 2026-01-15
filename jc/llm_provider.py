"""
JC-Agent LLM Integration Module

Provides a modular interface for calling different LLM providers (OpenAI, OpenRouter, HuggingFace, etc.), with error handling, logging, guardrails, memory/context, and tool-calling support.
"""
from __future__ import annotations

import json
import logging
from typing import Sequence

import requests

from .secrets import (
    get_effective_provider,
    get_llm_key_info,
    get_llm_model,
    load_env,
)
from .usage_logger import UsageLogger
from .key_locker import KeyLocker
from .error_handling import retry_with_backoff, CircuitBreaker
from .logging_config import get_logger


# Create circuit breaker for LLM calls (shared across all instances)
llm_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)


class LLMProvider:
    def __init__(self, provider: str | None = None, api_key: str | None = None, model: str | None = None, guardrails_manager=None):
        try:
            load_env()
        except Exception:
            pass

        self.provider = provider or get_effective_provider()
        key_info = get_llm_key_info(self.provider)
        self._key_info = key_info
        self.api_key = api_key or key_info.api_key
        if key_info.provider:
            self.provider = key_info.provider
        self.model = model or get_llm_model(self.provider)
        self.guardrails_manager = guardrails_manager
        self.logger = get_logger(__name__)

    def call(self, messages, models=None, tools=None, tool_choice=None, context=None, max_tokens=512, temperature=0.7, stream=False, personality=None):
        prepared_messages = self._prepare_messages(messages, personality)
        try:
            if not self.api_key:
                raise ValueError(f"No API key available for provider {self.provider}")

            if self.provider == "openai":
                if stream:
                    self.logger.warning("Streaming not supported for OpenAI yet; returning full response.")
                result = self._call_openai(prepared_messages, max_tokens, temperature)
            elif self.provider == "huggingface":
                if stream:
                    self.logger.warning("Streaming not supported for HuggingFace yet; returning full response.")
                result = self._call_huggingface(prepared_messages, max_tokens, temperature)
            else:
                result = self._call_openrouter(
                    prepared_messages,
                    models,
                    tools,
                    tool_choice,
                    context,
                    max_tokens,
                    temperature,
                    stream,
                )

            if self.guardrails_manager:
                result = self.guardrails_manager.apply(result)
            return result
        except Exception as exc:
            self.logger.error("LLM API error: %s", exc)
            return "Sorry, I couldn't process your request right now."

    def _prepare_messages(self, messages: Sequence[dict], personality: str | None) -> list[dict]:
        payload_messages = [dict(m) for m in messages]
        if personality:
            payload_messages.insert(0, {"role": "system", "content": f"You are {personality}."})
        return payload_messages

    @retry_with_backoff(max_attempts=3, exceptions=(requests.exceptions.RequestException, requests.exceptions.Timeout))
    def _call_openrouter(self, messages, models, tools, tool_choice, context, max_tokens, temperature, stream):
        with llm_circuit_breaker:
            payload = {
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": stream,
            }
            if models:
                payload["models"] = models
            else:
                payload["models"] = [self.model]
            if tools:
                payload["tools"] = tools
            if tool_choice:
                payload["tool_choice"] = tool_choice
            if context:
                payload["context"] = context

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=30,
                stream=stream,
            )
            response.raise_for_status()

            if stream:
                result = ""
                for chunk in response.iter_lines():
                    if chunk:
                        part = chunk.decode("utf-8")
                        result += part
                self._record_usage(result, operation="openrouter")
                return result

            data = response.json()
            result = data["choices"][0]["message"]["content"]
            self._record_usage(result, operation="openrouter")
            return result

    def _call_openai(self, messages, max_tokens, temperature):
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        result = data["choices"][0]["message"]["content"]
        self._record_usage(result, operation="openai")
        return result

    @retry_with_backoff(max_attempts=3, exceptions=(requests.exceptions.RequestException,))
    def _call_huggingface(self, messages, max_tokens, temperature):
        with llm_circuit_breaker:
            prompt = self._build_huggingface_prompt(messages)
            url = f"https://api-inference.huggingface.co/models/{self.model}"
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                },
                "options": {"wait_for_model": True},
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            result = self._extract_huggingface_text(data)
            self._record_usage(result, operation="huggingface")
            return result

    def _record_usage(self, response: str, operation: str) -> None:
        if not self._key_info or not self._key_info.key_id:
            return
        tokens = max(len(response.split()), 1)
        UsageLogger.log(
            key_id=self._key_info.key_id,
            name=self._key_info.provider,
            provider=self.provider,
            operation=operation,
            tokens=tokens,
            estimated_cost_usd=0.0,
        )
        KeyLocker.touch_key(self._key_info.key_id)

    @staticmethod
    def _build_huggingface_prompt(messages: Sequence[dict]) -> str:
        return "\n".join(
            f"{msg.get('role', 'user').capitalize()}: {msg.get('content', '').strip()}" for msg in messages if msg.get("content")
        )

    @staticmethod
    def _extract_huggingface_text(payload) -> str:
        if isinstance(payload, list) and payload:
            first = payload[0]
            if isinstance(first, dict):
                for field in ("generated_text", "text", "output", "result"):
                    value = first.get(field)
                    if value:
                        return value if isinstance(value, str) else value[0]
            elif isinstance(first, str):
                return first
        elif isinstance(payload, dict):
            for field in ("generated_text", "text", "output", "result"):
                value = payload.get(field)
                if value:
                    if isinstance(value, str):
                        return value
                    if isinstance(value, Sequence):
                        return value[0]

        raise ValueError("HuggingFace model did not return any text.")


# Example usage in JC-Agent:
# llm = LLMProvider(api_key="sk-xxx", model="ft:gpt-4.1-nano-2025-04-14:openai::BTz2REMH", guardrails_manager=guardrails)
# messages = [{"role": "user", "content": "What is the meaning of life?"}]
# result = llm.call(messages)
# print(result)
