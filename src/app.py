from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from adapters.input.api.establishments import api as establishments_api, init_api as init_establishments_api
from adapters.input.api.tags import api as tags_api, init_api as init_tags_api
from adapters.output.persistence.sqlalchemy.repositories.establishment_repository import SQLAlchemyEstablishmentRepository
from adapters.output.persistence.sqlalchemy.repositories.tag_repository import SQLAlchemyTagRepository
from domain.services.establishment_service import EstablishmentService
from domain.services.tag_service import TagService

# Import models
from adapters.output.persistence.sqlalchemy.models.establishment import EstablishmentModel, EstablishmentTagModel
from adapters.output.persistence.sqlalchemy.models.tag import TagModel, TagRelationshipModel
from adapters.output.persistence.sqlalchemy.models.base import Base
from infrastructure.config import Config

# Initialize extensions
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure SQLAlchemy from Config
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Create API
    api = Api(
        app,
        title="Mood Establishments API",
        version="1.0",
        description="API for searching establishments by mood"
    )
    
    # Initialize repositories and services
    tag_repository = SQLAlchemyTagRepository(db.session)
    tag_service = TagService(tag_repository)
    
    establishment_repository = SQLAlchemyEstablishmentRepository(db.session)
    establishment_service = EstablishmentService(
        establishment_repository=establishment_repository,
        tag_service=tag_service
    )
    
    # Initialize APIs with dependencies
    init_establishments_api(establishment_service)
    init_tags_api(tag_service)
    
    # Register namespaces
    api.add_namespace(establishments_api, path="/establishments")
    api.add_namespace(tags_api, path="/tags")
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 