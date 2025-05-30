import datetime
import os
from functools import wraps
from typing import Any, Callable, Optional

import bcrypt
import jwt
from flask import Response, request, session

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def generate_jwt(session_id: str, expires_in: int = 3600) -> str:
    """Generate a JWT token with session_id."""
    payload = {
        "session_id": session_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> Optional[dict[str, Any]]:
    """Decode and verify a JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def set_cookie(response: Response, key: str, value: str) -> Response:
    """Set a secure cookie in the response."""
    response.set_cookie(
        key,
        value,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=3600  # 1 hour
    )
    return response


def login_required(f: Callable) -> Callable:
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        token = request.cookies.get("access_token")
        if not token:
            return {"message": "No token provided"}, 401

        payload = decode_jwt(token)
        if not payload:
            return {"message": "Invalid or expired token"}, 401

        session_id = payload.get("session_id")
        if not session_id or session_id != session.get("session_id"):
            return {"message": "Invalid session"}, 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f: Callable) -> Callable:
    """Decorator to protect routes that require admin privileges."""
    @wraps(f)
    @login_required
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if not session.get("is_admin"):
            return {"message": "Admin privileges required"}, 403
        return f(*args, **kwargs)
    return decorated 