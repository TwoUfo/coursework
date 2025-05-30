import pytest
import json
from flask import url_for
from domain.models.user import User


def test_register_success(client, session):
    """Test successful user registration."""
    data = {"email": "test@example.com", "password": "test123", "is_admin": False}

    response = client.post("/auth/register", json=data)
    assert response.status_code == 201

    user = session.query(User).filter_by(email="test@example.com").first()
    assert user is not None
    assert user.email == "test@example.com"
    assert not user.is_admin


def test_register_duplicate_email(client, session):
    """Test registration with duplicate email."""
    # Create initial user
    user = User(email="test@example.com", password_hash="hash123", is_admin=False)
    session.add(user)
    session.commit()

    data = {"email": "test@example.com", "password": "test123", "is_admin": False}

    response = client.post("/auth/register", json=data)
    assert response.status_code == 400
    assert b"Email already exists" in response.data


def test_login_success(client, session):
    """Test successful login."""
    # Create user
    user = User(email="test@example.com", password_hash="hash123", is_admin=False)
    session.add(user)
    session.commit()

    data = {"email": "test@example.com", "password": "test123"}

    response = client.post("/auth/login", json=data)
    assert response.status_code == 200

    # Check response contains tokens
    response_data = json.loads(response.data)
    assert "access_token" in response_data
    assert "refresh_token" in response_data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    data = {"email": "wrong@example.com", "password": "wrong123"}

    response = client.post("/auth/login", json=data)
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data


def test_refresh_token_success(client, auth_headers):
    """Test successful token refresh."""
    response = client.post("/auth/refresh", headers=auth_headers)
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert "access_token" in response_data


def test_refresh_token_invalid(client):
    """Test token refresh with invalid token."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.post("/auth/refresh", headers=headers)
    assert response.status_code == 401


def test_logout_success(client, auth_headers):
    """Test successful logout."""
    response = client.post("/auth/logout", headers=auth_headers)
    assert response.status_code == 200


def test_protected_route_with_token(client, auth_headers):
    """Test accessing protected route with valid token."""
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200


def test_protected_route_without_token(client):
    """Test accessing protected route without token."""
    response = client.get("/protected")
    assert response.status_code == 401


def test_admin_route_with_admin_token(client, session):
    """Test accessing admin route with admin token."""
    # Create admin user and generate token
    admin = User(email="admin@example.com", password_hash="hash123", is_admin=True)
    session.add(admin)
    session.commit()

    headers = {"Authorization": "Bearer admin-token"}
    response = client.get("/admin", headers=headers)
    assert response.status_code == 200


def test_admin_route_with_user_token(client, session):
    """Test accessing admin route with non-admin token."""
    # Create regular user and generate token
    user = User(email="user@example.com", password_hash="hash123", is_admin=False)
    session.add(user)
    session.commit()

    headers = {"Authorization": "Bearer user-token"}
    response = client.get("/admin", headers=headers)
    assert response.status_code == 403
