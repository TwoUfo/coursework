from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from domain.models.establishment import Establishment, EstablishmentTag
from .base import Base


class EstablishmentModel(Base):
    """SQLAlchemy model for establishments."""

    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    tags = relationship("EstablishmentTagModel", back_populates="establishment")
    _score = None  # Transient attribute for score

    def to_domain(self) -> Establishment:
        """Convert to domain model."""
        return Establishment(
            id=self.id,
            name=self.name,
            description=self.description,
            tags=[tag.to_domain() for tag in self.tags],
            score=self._score,
        )

    @staticmethod
    def from_domain(establishment: Establishment) -> "EstablishmentModel":
        """Create from domain model."""
        model = EstablishmentModel(
            id=establishment.id,
            name=establishment.name,
            description=establishment.description,
        )
        model._score = establishment.score
        return model


class EstablishmentTagModel(Base):
    """SQLAlchemy model for establishment tags."""

    __tablename__ = "establishment_tags"

    establishment_id = Column(
        Integer, ForeignKey("establishments.id"), primary_key=True
    )
    tag_name = Column(String(50), ForeignKey("tags.name"), primary_key=True)
    count = Column(Integer, default=1)

    establishment = relationship("EstablishmentModel", back_populates="tags")
    tag = relationship("TagModel")

    def to_domain(self) -> EstablishmentTag:
        """Convert to domain model."""
        return EstablishmentTag(tag_name=self.tag_name, count=self.count)
