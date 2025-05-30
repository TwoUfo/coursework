"""Main application module."""
from flask import Flask
from flask_jwt_extended import JWTManager
from infrastructure.database import db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure the Flask-JWT-Extended extension
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    jwt = JWTManager(app)
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 