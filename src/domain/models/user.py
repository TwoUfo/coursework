from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    is_admin: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "is_admin": self.is_admin
        } 