import uuid
from typing import Optional

from flask import session

from adapters.output.persistence.sqlalchemy.models.user import UserModel
from domain.models.user import User


def get_user_by_email(email: str) -> Optional[User]:
    """
    Retrieves a user from the database by email.
    
    Args:
        email (str): The email of the user.
    
    Returns:
        Optional[User]: The user if found, None otherwise.
    """
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        return None
    return user.to_domain()


def get_session_id() -> str:
    """
    Retrieves or generates a session ID.
    
    Returns:
        str: The session ID.
    """
    session_id = session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id
    return session_id 