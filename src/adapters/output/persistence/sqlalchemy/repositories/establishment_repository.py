from typing import List, Optional, Dict

from sqlalchemy import func, case, Float, cast, and_, or_
from sqlalchemy.orm import Session, joinedload

from adapters.output.persistence.sqlalchemy.models.establishment import (
    EstablishmentModel,
    EstablishmentTagModel,
)
from adapters.output.persistence.sqlalchemy.models.tag import TagRelationshipModel
from domain.models.establishment import Establishment, EstablishmentTag
from domain.ports.output.establishment_repository import EstablishmentRepositoryPort


class SQLAlchemyEstablishmentRepository(EstablishmentRepositoryPort):
    """SQLAlchemy implementation of EstablishmentRepositoryPort."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, establishment: Establishment) -> Establishment:
        """Save an establishment to the database."""
        establishment_model = EstablishmentModel.from_domain(establishment)
        self.session.add(establishment_model)
        self.session.commit()
        return establishment_model.to_domain()

    def get_by_id(self, establishment_id: int) -> Optional[Establishment]:
        """Get an establishment by ID."""
        establishment_model = (
            self.session.query(EstablishmentModel)
            .options(joinedload(EstablishmentModel.tags))
            .get(establishment_id)
        )
        return establishment_model.to_domain() if establishment_model else None

    def add_tag(self, establishment_id: int, tag_name: str) -> EstablishmentTag:
        """Add or increment a tag count for an establishment."""
        tag_model = (
            self.session.query(EstablishmentTagModel)
            .filter_by(establishment_id=establishment_id, tag_name=tag_name)
            .first()
        )

        if tag_model:
            tag_model.count += 1
        else:
            tag_model = EstablishmentTagModel(
                establishment_id=establishment_id, tag_name=tag_name, count=1
            )
            self.session.add(tag_model)

        self.session.commit()
        return tag_model.to_domain()

    def get_by_tags(
        self, tag_weights: Dict[str, float], limit: int = 10
    ) -> List[Establishment]:
        """
        Get establishments by tags and their weights, considering tag relationships.

        This implementation:
        1. Finds direct tag matches and their related tags
        2. Calculates scores based on both direct matches and related tags
        3. Orders results by the total weighted score
        4. Returns the top N results with their scores
        """
        direct_score_cases = []
        for tag_name, weight in tag_weights.items():
            direct_score_cases.append(
                case(
                    (
                        EstablishmentTagModel.tag_name == tag_name,
                        cast(EstablishmentTagModel.count * weight, Float),
                    ),
                    else_=cast(0.0, Float),
                )
            )

        direct_score = func.sum(func.coalesce(sum(direct_score_cases), 0.0))

        related_score_cases = []
        for tag_name, weight in tag_weights.items():
            related_score_cases.append(
                case(
                    (
                        and_(
                            TagRelationshipModel.source_tag_name == tag_name,
                            EstablishmentTagModel.tag_name
                            == TagRelationshipModel.target_tag_name,
                        ),
                        cast(
                            EstablishmentTagModel.count
                            * TagRelationshipModel.weight
                            * weight,
                            Float,
                        ),
                    ),
                    else_=cast(0.0, Float),
                )
            )

        related_score = func.sum(func.coalesce(sum(related_score_cases), 0.0))

        total_score = (direct_score + related_score).label("total_score")

        query = (
            self.session.query(EstablishmentModel, total_score)
            .join(EstablishmentTagModel)
            .outerjoin(
                TagRelationshipModel,
                and_(
                    TagRelationshipModel.source_tag_name.in_(tag_weights.keys()),
                    EstablishmentTagModel.tag_name
                    == TagRelationshipModel.target_tag_name,
                ),
            )
            .filter(
                or_(
                    EstablishmentTagModel.tag_name.in_(tag_weights.keys()),
                    and_(
                        TagRelationshipModel.source_tag_name.in_(tag_weights.keys()),
                        EstablishmentTagModel.tag_name
                        == TagRelationshipModel.target_tag_name,
                    ),
                )
            )
            .group_by(EstablishmentModel)
            .having(total_score > 0)
            .order_by(total_score.desc())
            .limit(limit)
        )

        results = query.options(joinedload(EstablishmentModel.tags)).all()

        establishments = []
        for establishment_model, score in results:
            establishment_model._score = float(score)
            establishments.append(establishment_model.to_domain())

        return establishments
