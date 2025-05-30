from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database import db
from domain.models.comment import Comment


class CommentModel(db.Model):
    """SQLAlchemy model for comments."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    establishment_id = Column(Integer, ForeignKey("establishments.id"), nullable=False)
    text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    establishment = relationship("EstablishmentModel", back_populates="comments")

    def to_domain(self) -> Comment:
        """Convert to domain model."""
        return Comment(
            id=self.id,
            establishment_id=self.establishment_id,
            text=self.text,
            rating=self.rating,
            created_at=self.created_at,
        )

    @staticmethod
    def from_domain(comment: Comment) -> "CommentModel":
        """Create from domain model."""
        return CommentModel(
            id=comment.id,
            establishment_id=comment.establishment_id,
            text=comment.text,
            rating=comment.rating,
            created_at=comment.created_at,
        ) 