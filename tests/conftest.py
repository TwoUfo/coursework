import os
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from infrastructure.database import db as _db
from app import create_app


@pytest.fixture(scope="session")
def app():
    """Create and configure a test Flask application."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    app.config["SECRET_KEY"] = "test-secret-key"

    return app


@pytest.fixture(scope="session")
def db(app):
    """Create and configure a test database."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(scope="function")
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Create authentication headers for testing."""
    return {"Authorization": "Bearer test-token"}
