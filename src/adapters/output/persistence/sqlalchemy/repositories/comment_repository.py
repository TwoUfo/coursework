from typing import List
from sqlalchemy.orm import Session

from domain.models.comment import Comment
from domain.ports.output.comment_repository import CommentRepositoryPort
from adapters.output.persistence.sqlalchemy.models.comment import CommentModel


class SQLAlchemyCommentRepository(CommentRepositoryPort):
    """SQLAlchemy implementation of CommentRepositoryPort."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, comment: Comment) -> Comment:
        """Save a comment to the database."""
        comment_model = CommentModel.from_domain(comment)
        self.session.add(comment_model)
        self.session.commit()
        return comment_model.to_domain()

    def get_by_establishment_id(self, establishment_id: int) -> List[Comment]:
        """Get all comments for an establishment."""
        comment_models = (
            self.session.query(CommentModel)
            .filter_by(establishment_id=establishment_id)
            .all()
        )
        return [model.to_domain() for model in comment_models] 