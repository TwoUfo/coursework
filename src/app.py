from flask import Flask
from flask_restx import Api

from adapters.input.api.establishments import (
    api as establishments_api,
    init_api as init_establishments_api,
)
from adapters.input.api.tags import api as tags_api, init_api as init_tags_api
from adapters.input.api.auth.routes import api as auth_api
from adapters.output.persistence.sqlalchemy.repositories.establishment_repository import (
    SQLAlchemyEstablishmentRepository,
)
from adapters.output.persistence.sqlalchemy.repositories.tag_repository import (
    SQLAlchemyTagRepository,
)
from domain.services.establishment_service import EstablishmentService
from domain.services.tag_service import TagService

from adapters.output.persistence.sqlalchemy.models.establishment import (
    EstablishmentModel,
    EstablishmentTagModel,
)
from adapters.output.persistence.sqlalchemy.models.tag import (
    TagModel,
    TagRelationshipModel,
)
from infrastructure.config import Config
from infrastructure.database import db, migrate


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Create API
    api = Api(
        app,
        title="Mood Establishments API",
        version="1.0",
        description="API for searching establishments by mood",
    )

    # Initialize services
    tag_repository = SQLAlchemyTagRepository(db.session)
    tag_service = TagService(tag_repository)

    establishment_repository = SQLAlchemyEstablishmentRepository(db.session)
    establishment_service = EstablishmentService(
        establishment_repository=establishment_repository, tag_service=tag_service
    )

    # Initialize and register APIs
    init_establishments_api(establishment_service)
    init_tags_api(tag_service)

    api.add_namespace(establishments_api, path="/establishments")
    api.add_namespace(tags_api, path="/tags")
    api.add_namespace(auth_api, path="/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
