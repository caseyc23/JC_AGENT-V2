"""API Authentication for JC Agent.

Provides JWT token-based authentication and API key validation for secure endpoint access.
"""
from __future__ import annotations

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Security configuration
SECRET_KEY = os.getenv("JC_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# API key from environment
API_KEY = os.getenv("JC_API_KEY", "")

# Password hashing - using pbkdf2_sha256 for Python 3.13 compatibility
# Note: Bcrypt has issues with passlib on Python 3.13
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Security schemes
bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class TokenData(BaseModel):
    """JWT token payload."""
    username: Optional[str] = None
    scopes: list[str] = []


class User(BaseModel):
    """User model for authentication."""
    username: str
    scopes: list[str] = []


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token.
    
    Args:
        data: Payload data to encode
        expires_delta: Optional expiration time delta
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token data
    
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username, scopes=payload.get("scopes", []))
        return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
    api_key: Optional[str] = Security(api_key_header),
) -> Optional[User]:
    """Get current user from JWT token or API key (optional, returns None if not authenticated).
    
    Checks both Bearer token and X-API-Key header.
    
    Args:
        credentials: HTTP Bearer token credentials
        api_key: API key from header
    
    Returns:
        User object if authenticated, None otherwise
    """
    # If authentication is disabled (no API_KEY set), allow access
    if not API_KEY:
        return User(username="anonymous", scopes=["public"])
    
    # Check API key first
    if api_key and api_key == API_KEY:
        return User(username="api_key_user", scopes=["admin"])
    
    # Check Bearer token
    if credentials:
        token_data = verify_token(credentials.credentials)
        return User(username=token_data.username, scopes=token_data.scopes)
    
    return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
    api_key: Optional[str] = Security(api_key_header),
) -> User:
    """Get current user from JWT token or API key (required).
    
    Checks both Bearer token and X-API-Key header.
    
    Args:
        credentials: HTTP Bearer token credentials
        api_key: API key from header
    
    Returns:
        User object
    
    Raises:
        HTTPException: If not authenticated
    """
    user = await get_current_user_optional(credentials, api_key)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide Bearer token or X-API-Key header.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def hash_password(password: str) -> str:
    """Hash a password for storage.
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
    
    Returns:
        True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)
