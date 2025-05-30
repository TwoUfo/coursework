import os
from datetime import timedelta


class Config:
    """Base configuration class."""

    # Database
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/coursework"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
