"""FastAPI router that exposes the Key Locker HTTP API."""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from .key_locker import KeyLocker
from .usage_logger import UsageLogger

router = APIRouter(prefix="/keys", tags=["keys"])


class KeyPayload(BaseModel):
    name: str
    provider: str
    secret: str
    budget: float | None = None
    passphrase: str | None = None
    notes: str | None = None


class KeyEditPayload(BaseModel):
    id: str
    name: str | None = None
    provider: str | None = None
    budget: float | None = None
    secret: str | None = None
    passphrase: str | None = None


class KeyIdPayload(BaseModel):
    id: str
    passphrase: str | None = None


@router.post("/add")
def add_key(payload: KeyPayload) -> dict[str, Any]:
    try:
        metadata = KeyLocker.add_key(
            name=payload.name,
            provider=payload.provider,
            secret=payload.secret,
            budget_usd=payload.budget,
            passphrase=payload.passphrase,
            notes=payload.notes,
        )
        return {"ok": True, "key": metadata}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/list")
def list_keys(passphrase: Optional[str] = Query(None, description="Passphrase for encrypted storage (if keyring is unavailable)")) -> dict[str, Any]:
    try:
        keys = KeyLocker.list_keys(passphrase=passphrase)
        enriched: list[dict[str, Any]] = []
        for entry in keys:
            summary = UsageLogger.summary(entry["id"], days=30, max_entries=0)
            enriched.append(
                {
                    **entry,
                    "usage_summary": {
                        "total_tokens": summary["total_tokens"],
                        "total_estimated_usd": summary["total_estimated_usd"],
                    },
                }
            )
        return {"keys": enriched}
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.post("/delete")
def delete_key(payload: KeyIdPayload) -> dict[str, bool]:
    try:
        KeyLocker.delete_key(payload.id, passphrase=payload.passphrase)
        return {"deleted": True}
    except KeyError:
        raise HTTPException(status_code=404, detail="Key not found")
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.post("/edit")
def edit_key(payload: KeyEditPayload) -> dict[str, Any]:
    try:
        entry = KeyLocker.edit_key(
            key_id=payload.id,
            name=payload.name,
            provider=payload.provider,
            budget_usd=payload.budget,
            secret=payload.secret,
            passphrase=payload.passphrase,
        )
        return {"ok": True, "key": entry}
    except KeyError:
        raise HTTPException(status_code=404, detail="Key not found")
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.post("/get-secret")
def get_secret(payload: KeyIdPayload) -> dict[str, str]:
    try:
        secret = KeyLocker.get_secret(payload.id, passphrase=payload.passphrase)
        return {"secret": secret}
    except KeyError:
        raise HTTPException(status_code=404, detail="Key not found")
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.get("/usage/{key_id}")
def usage(key_id: str, days: int = Query(30, ge=0)) -> dict[str, Any]:
    summary = UsageLogger.summary(key_id, days=days)
    if summary["entries"]:
        return summary
    return {**summary, "entries": []}


@router.get("/discover")
def discover_key(provider: str, passphrase: Optional[str] = Query(None)) -> dict[str, Any]:
    key = KeyLocker.find_key_for_provider(provider, passphrase=passphrase)
    if not key:
        raise HTTPException(status_code=404, detail="No key found for provider")
    return {"key": key}
