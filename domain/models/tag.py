"""Tag models module."""
from infrastructure.database import db


class Tag(db.Model):
    """Tag model."""
    
    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(200))
    
    def __str__(self):
        """String representation."""
        return f"<Tag {self.name}>"


class TagRelationship(db.Model):
    """Tag relationship model."""
    
    id = db.Column(db.Integer, primary_key=True)
    source_tag_name = db.Column(db.String(50), db.ForeignKey('tag.name'), nullable=False)
    target_tag_name = db.Column(db.String(50), db.ForeignKey('tag.name'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    
    def __str__(self):
        """String representation."""
        return f"<TagRelationship {self.source_tag_name} -> {self.target_tag_name} ({self.weight})>" 