import os
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher

password_hasher = PasswordHasher()
SECRET_KEY = os.getenv("SECRET_KEY", "MiPasswordSeguro123@")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Generate a secure hash for the given plain-text password."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify that the plain-text password matches the hashed password."""
    return password_hasher.verify(password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with an expiration time."""
    to_encode: dict[str, Any] = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore[reportUnknownMemberType]

    return encoded_jwt


def verify_access_token(token: str) -> dict[str, Any] | None:
    """Decode and verify a JWT access token, returning its payload if valid."""
    try:
        payload: dict[str, Any] = jwt.decode( # type: ignore
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.InvalidTokenError:
        return None
