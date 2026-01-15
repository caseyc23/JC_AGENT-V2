"""Lightweight usage logging for Key Locker analytics."""
from __future__ import annotations

import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .key_locker import STORAGE_PATH

_USAGE_LOG = STORAGE_PATH / "usage.log"
_USAGE_LOCK = threading.Lock()


def _ensure_usage_log() -> None:
    if not _USAGE_LOG.exists():
        STORAGE_PATH.mkdir(parents=True, exist_ok=True)
        _USAGE_LOG.write_text("", encoding="utf-8")
        _USAGE_LOG.chmod(0o600)


class UsageLogger:
    @classmethod
    def log(
        cls,
        key_id: str,
        name: str | None = None,
        provider: str | None = None,
        operation: str | None = None,
        tokens: int | None = None,
        estimated_cost_usd: float | None = None,
        meta: Any | None = None,
    ) -> None:
        _ensure_usage_log()
        entry = {
            "at": datetime.utcnow().isoformat() + "Z",
            "key_id": key_id,
            "name": name,
            "provider": provider,
            "operation": operation,
            "tokens": tokens,
            "estimated_cost_usd": estimated_cost_usd,
            "meta": meta,
        }
        with _USAGE_LOCK:
            with open(_USAGE_LOG, "a", encoding="utf-8") as stream:
                stream.write(json.dumps(entry, default=str) + "\n")

    @classmethod
    def summary(cls, key_id: str, days: int = 30, max_entries: int = 20) -> dict[str, Any]:
        _ensure_usage_log()
        cutoff = datetime.utcnow() - timedelta(days=max(days, 0))
        entries: list[dict[str, Any]] = []
        total_tokens = 0
        total_estimated = 0.0
        with _USAGE_LOCK:
            for line in _USAGE_LOG.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if data.get("key_id") != key_id:
                    continue
                recorded = data.get("at")
                try:
                    recorded_time = datetime.fromisoformat(recorded.replace("Z", ""))
                except Exception:  # pragma: no cover - best effort
                    recorded_time = None
                if recorded_time and recorded_time < cutoff:
                    continue
                entries.append(data)
                if data.get("tokens"):
                    total_tokens += data["tokens"]
                if data.get("estimated_cost_usd"):
                    total_estimated += data["estimated_cost_usd"]
        if max_entries > 0:
            entries = entries[-max_entries:]
        else:
            entries = []
        return {
            "key_id": key_id,
            "days": days,
            "total_tokens": total_tokens,
            "total_estimated_usd": round(total_estimated, 6),
            "entries": entries,
        }


__all__ = ["UsageLogger"]
