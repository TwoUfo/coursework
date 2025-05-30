"""Establishment models module."""
from datetime import datetime
from infrastructure.database import db


class Establishment(db.Model):
    """Establishment model."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float)
    tags = db.relationship('EstablishmentTag', backref='establishment', lazy=True)
    
    def __str__(self):
        """String representation."""
        return f"<Establishment {self.name}>"


class EstablishmentTag(db.Model):
    """Establishment tag model."""
    
    id = db.Column(db.Integer, primary_key=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishment.id'), nullable=False)
    tag_name = db.Column(db.String(50), db.ForeignKey('tag.name'), nullable=False)
    count = db.Column(db.Integer, default=1) 