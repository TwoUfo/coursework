from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    """Domain model for Comment."""

    id: Optional[int]
    establishment_id: int
    text: str
    rating: int  # Rating from 1 to 10
    created_at: datetime = datetime.utcnow()

    def __str__(self) -> str:
        return f"<Comment {self.id} for establishment {self.establishment_id}>" 