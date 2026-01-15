"""Secure key locker utilities for JC Agent."""
from __future__ import annotations

import base64
import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    import keyring
except ImportError:  # pragma: no cover - keyring optional
    keyring = None

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError as exc:  # pragma: no cover - must add to requirements
    raise ImportError("cryptography is required for encrypted secrets fallback") from exc

_STORAGE_BASE = Path(os.getenv("JC_STORAGE_PATH") or Path.home() / ".jc-agent")
_STORAGE_BASE.mkdir(parents=True, exist_ok=True)

STORAGE_PATH = _STORAGE_BASE
_METADATA_FILE = STORAGE_PATH / "keys-meta.json"
_SECRETS_FILE = STORAGE_PATH / "secrets.enc"
_AUDIT_LOG = STORAGE_PATH / "keys-audit.log"

_SERVICE_NAME = "JC Agent Key Locker"
_METADATA_LOCK = threading.Lock()

_REPEATABLE_SALT_BYTES = 16
_KDF_ITERATIONS = 390_000


@dataclass
class KeyMetadata:
    id: str
    name: str
    provider: str
    created_at: str
    storage: str
    budget_usd: float | None = None
    notes: str | None = None
    last_used_at: str | None = None
    updated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _ensure_metadata_file() -> None:
    if not _METADATA_FILE.exists():
        _METADATA_FILE.write_text("{}", encoding="utf-8")
        _METADATA_FILE.chmod(0o600)


def _read_metadata() -> dict[str, dict[str, Any]]:
    _ensure_metadata_file()
    try:
        content = _METADATA_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError:
        return {}


def _write_metadata(raw: dict[str, dict[str, Any]]) -> None:
    _METADATA_FILE.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    _METADATA_FILE.chmod(0o600)


def _ensure_audit_log() -> None:
    if not _AUDIT_LOG.exists():
        _AUDIT_LOG.write_text("", encoding="utf-8")
        _AUDIT_LOG.chmod(0o600)


def _audit(action: str, key_id: str, data: dict[str, Any]) -> None:
    _ensure_audit_log()
    entry = {
        "at": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "key_id": key_id,
        "data": data,
    }
    with open(_AUDIT_LOG, "a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry) + "\n")


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=_KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))


def _encrypt_payload(payload: dict[str, str], passphrase: str) -> dict[str, str]:
    salt = os.urandom(_REPEATABLE_SALT_BYTES)
    key = _derive_key(passphrase, salt)
    fernet = Fernet(key)
    token = fernet.encrypt(json.dumps(payload).encode("utf-8"))
    return {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "payload": token.decode("utf-8"),
    }


def _decrypt_payload(contents: dict[str, str], passphrase: str) -> dict[str, str]:
    salt = base64.b64decode(contents["salt"])
    key = _derive_key(passphrase, salt)
    fernet = Fernet(key)
    payload = fernet.decrypt(contents["payload"].encode("utf-8"))
    return json.loads(payload.decode("utf-8"))


def _require_passphrase(passphrase: str | None) -> str:
    resolved = passphrase or os.getenv("JC_SECRETS_PASSPHRASE")
    if not resolved:
        raise ValueError("Passphrase required for encrypted key storage")
    return resolved


def _load_secret_map(passphrase: str) -> dict[str, str]:
    if not _SECRETS_FILE.exists():
        return {}
    contents = json.loads(_SECRETS_FILE.read_text(encoding="utf-8"))
    return _decrypt_payload(contents, passphrase)


def _write_secret_map(map_data: dict[str, str], passphrase: str) -> None:
    _SECRETS_FILE.write_text(json.dumps(_encrypt_payload(map_data, passphrase)), encoding="utf-8")
    _SECRETS_FILE.chmod(0o600)


def _set_secret_file_value(key_id: str, secret: str, passphrase: str) -> None:
    data = _load_secret_map(passphrase)
    data[key_id] = secret
    _write_secret_map(data, passphrase)


def _delete_secret_file_value(key_id: str, passphrase: str) -> None:
    data = _load_secret_map(passphrase)
    if key_id in data:
        del data[key_id]
        _write_secret_map(data, passphrase)


def _get_secret_file_value(key_id: str, passphrase: str) -> Optional[str]:
    data = _load_secret_map(passphrase)
    return data.get(key_id)


class KeyLocker:
    """Central key storage API."""

    @classmethod
    def using_keyring(cls) -> bool:
        return keyring is not None

    @classmethod
    def _pick_storage(cls) -> str:
        return "keyring" if cls.using_keyring() else "file"

    @classmethod
    def _sanitize_provider(cls, provider: str) -> str:
        return provider.strip().lower()

    @classmethod
    def add_key(
        cls,
        name: str,
        provider: str,
        secret: str,
        budget_usd: float | None = None,
        passphrase: str | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        if not name.strip():
            raise ValueError("Key name is required")
        if not provider.strip():
            raise ValueError("Provider is required")
        if not secret:
            raise ValueError("Secret value is required")

        storage = cls._pick_storage()
        key_id = uuid.uuid4().hex
        now = datetime.utcnow().isoformat() + "Z"
        metadata = KeyMetadata(
            id=key_id,
            name=name.strip(),
            provider=cls._sanitize_provider(provider),
            created_at=now,
            storage=storage,
            budget_usd=budget_usd,
            notes=notes,
        )

        if storage == "keyring":
            keyring.set_password(_SERVICE_NAME, key_id, secret)
        else:
            resolved = _require_passphrase(passphrase)
            _set_secret_file_value(key_id, secret, resolved)

        with _METADATA_LOCK:
            data = _read_metadata()
            data[key_id] = metadata.to_dict()
            _write_metadata(data)

        _audit("add", key_id, {"name": metadata.name, "provider": metadata.provider, "storage": storage})
        return metadata.to_dict()

    @classmethod
    def list_keys(cls, passphrase: str | None = None) -> List[dict[str, Any]]:
        if not cls.using_keyring():
            _require_passphrase(passphrase)
        with _METADATA_LOCK:
            data = _read_metadata()
        keys = list(data.values())
        keys.sort(key=lambda entry: entry.get("created_at", ""))
        return keys

    @classmethod
    def get_key(cls, key_id: str, passphrase: str | None = None) -> dict[str, Any]:
        with _METADATA_LOCK:
            data = _read_metadata()
            entry = data.get(key_id)
        if not entry:
            raise KeyError("Key not found")
        secret = cls.get_secret(key_id, passphrase=passphrase)
        result = dict(entry)
        result["secret_available"] = bool(secret)
        return result

    @classmethod
    def get_secret(cls, key_id: str, passphrase: str | None = None) -> str:
        with _METADATA_LOCK:
            data = _read_metadata()
            entry = data.get(key_id)
        if not entry:
            raise KeyError("Key not found")
        if entry.get("storage") == "keyring":
            if not keyring:
                raise RuntimeError("Keyring module not available")
            secret = keyring.get_password(_SERVICE_NAME, key_id)
        else:
            resolved = _require_passphrase(passphrase)
            secret = _get_secret_file_value(key_id, resolved)
        if not secret:
            raise ValueError("Secret missing or encrypted")
        return secret

    @classmethod
    def delete_key(cls, key_id: str, passphrase: str | None = None) -> None:
        with _METADATA_LOCK:
            data = _read_metadata()
            entry = data.pop(key_id, None)
            if entry is None:
                raise KeyError("Key not found")
            _write_metadata(data)
        storage = entry.get("storage")
        if storage == "keyring":
            if keyring:
                keyring.delete_password(_SERVICE_NAME, key_id)
        else:
            resolved = _require_passphrase(passphrase)
            _delete_secret_file_value(key_id, resolved)
        _audit("delete", key_id, {"name": entry.get("name"), "provider": entry.get("provider")})

    @classmethod
    def edit_key(
        cls,
        key_id: str,
        name: str | None = None,
        provider: str | None = None,
        budget_usd: float | None = None,
        secret: str | None = None,
        passphrase: str | None = None,
    ) -> dict[str, Any]:
        with _METADATA_LOCK:
            data = _read_metadata()
            entry = data.get(key_id)
            if not entry:
                raise KeyError("Key not found")
            if name:
                entry["name"] = name.strip()
            if provider:
                entry["provider"] = cls._sanitize_provider(provider)
            if budget_usd is not None:
                entry["budget_usd"] = budget_usd
            entry["updated_at"] = datetime.utcnow().isoformat() + "Z"
            data[key_id] = entry
            _write_metadata(data)
        if secret is not None:
            storage = entry.get("storage")
            if storage == "keyring":
                if not keyring:
                    raise RuntimeError("Keyring module not available")
                keyring.set_password(_SERVICE_NAME, key_id, secret)
            else:
                resolved = _require_passphrase(passphrase)
                _set_secret_file_value(key_id, secret, resolved)
        _audit("edit", key_id, {"name": entry.get("name"), "provider": entry.get("provider")})
        return entry

    @classmethod
    def find_key_for_provider(cls, provider: str, passphrase: str | None = None) -> dict[str, Any] | None:
        normalized = cls._sanitize_provider(provider)
        for entry in cls.list_keys(passphrase=passphrase):
            if entry.get("provider") == normalized:
                return entry
        return None

    @classmethod
    def touch_key(cls, key_id: str) -> None:
        with _METADATA_LOCK:
            data = _read_metadata()
            entry = data.get(key_id)
            if not entry:
                return
            entry["last_used_at"] = datetime.utcnow().isoformat() + "Z"
            data[key_id] = entry
            _write_metadata(data)


__all__ = ["KeyLocker", "KeyMetadata", "STORAGE_PATH"]
