"""Tests for authentication module."""
import os
import pytest
from datetime import timedelta
from jose import jwt

from jc.auth import (
    create_access_token,
    verify_token,
    hash_password,
    verify_password,
    TokenData,
    ALGORITHM,
    SECRET_KEY,
)


def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "testuser", "scopes": ["read", "write"]}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 20
    
    # Verify token can be decoded
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "exp" in payload


def test_create_access_token_with_expiry():
    """Test JWT token with custom expiration."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=5)
    token = create_access_token(data, expires_delta)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload


def test_verify_token_success():
    """Test successful token verification."""
    data = {"sub": "testuser", "scopes": ["read"]}
    token = create_access_token(data)
    
    token_data = verify_token(token)
    assert token_data.username == "testuser"
    assert token_data.scopes == ["read"]


def test_verify_token_invalid():
    """Test verification of invalid token."""
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException) as exc_info:
        verify_token("invalid.token.here")
    
    assert exc_info.value.status_code == 401


def test_hash_password():
    """Test password hashing."""
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 20
    assert hashed.startswith("$pbkdf2-sha256$")  # pbkdf2 hash prefix


def test_verify_password():
    """Test password verification."""
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_token_data_model():
    """Test TokenData model."""
    token_data = TokenData(username="testuser", scopes=["admin"])
    
    assert token_data.username == "testuser"
    assert token_data.scopes == ["admin"]
