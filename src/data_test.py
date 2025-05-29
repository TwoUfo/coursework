from flask import Flask
from app import create_app, db
from adapters.output.persistence.sqlalchemy.models.tag import TagModel, TagRelationshipModel
from adapters.output.persistence.sqlalchemy.models.establishment import EstablishmentModel, EstablishmentTagModel

def create_tags():
    """Create test mood tags."""
    tags = [
        # Basic moods
        {"name": "Happy", "description": "Feeling or showing pleasure or contentment"},
        {"name": "Excited", "description": "Very enthusiastic and eager"},
        {"name": "Relaxed", "description": "Free from tension and anxiety"},
        {"name": "Peaceful", "description": "Free from disturbance; tranquil"},
        {"name": "Romantic", "description": "Conducive to or characterized by romance"},
        
        # Social moods
        {"name": "Social", "description": "Seeking or enjoying companionship"},
        {"name": "Friendly", "description": "Warm and welcoming atmosphere"},
        {"name": "Party", "description": "Lively and festive environment"},
        {"name": "Intimate", "description": "Private and cozy setting"},
        {"name": "Networking", "description": "Professional and social connections"},
        
        # Activity-based moods
        {"name": "Energetic", "description": "Full of energy and enthusiasm"},
        {"name": "Creative", "description": "Inspiring artistic or innovative thinking"},
        {"name": "Focused", "description": "Conducive to concentration"},
        {"name": "Productive", "description": "Efficient and results-oriented"},
        {"name": "Adventurous", "description": "Exciting and potentially dangerous"},
        
        # Atmospheric moods
        {"name": "Cozy", "description": "Warm and comfortable"},
        {"name": "Elegant", "description": "Graceful and stylish"},
        {"name": "Modern", "description": "Contemporary and trendy"},
        {"name": "Traditional", "description": "Following established customs"},
        {"name": "Mysterious", "description": "Intriguing and enigmatic"}
    ]
    
    # Create and save tags
    for tag_data in tags:
        tag = TagModel(name=tag_data["name"], description=tag_data["description"])
        db.session.add(tag)
    
    db.session.commit()
    
    # Create relationships between tags with weights (0-1)
    relationships = [
        # Happy relationships
        ("Happy", "Excited", 0.8),
        ("Happy", "Social", 0.7),
        ("Happy", "Friendly", 0.9),
        ("Happy", "Party", 0.6),
        
        # Excited relationships
        ("Excited", "Energetic", 0.9),
        ("Excited", "Party", 0.8),
        ("Excited", "Adventurous", 0.7),
        
        # Relaxed relationships
        ("Relaxed", "Peaceful", 0.9),
        ("Relaxed", "Cozy", 0.8),
        ("Relaxed", "Focused", 0.6),
        
        # Social relationships
        ("Social", "Friendly", 0.9),
        ("Social", "Party", 0.8),
        ("Social", "Networking", 0.7),
        
        # Romantic relationships
        ("Romantic", "Intimate", 0.9),
        ("Romantic", "Elegant", 0.7),
        ("Romantic", "Cozy", 0.6),
        
        # Creative relationships
        ("Creative", "Modern", 0.7),
        ("Creative", "Mysterious", 0.5),
        ("Creative", "Energetic", 0.6),
        
        # Atmospheric connections
        ("Elegant", "Modern", 0.6),
        ("Traditional", "Cozy", 0.7),
        ("Mysterious", "Intimate", 0.5),
        
        # Activity connections
        ("Productive", "Focused", 0.8),
        ("Adventurous", "Energetic", 0.8),
        ("Party", "Energetic", 0.7)
    ]
    
    # Create relationships
    for source_name, target_name, weight in relationships:
        # Create bidirectional relationships with the same weight
        relationship1 = TagRelationshipModel(
            source_tag_name=source_name,
            target_tag_name=target_name,
            weight=weight
        )
        relationship2 = TagRelationshipModel(
            source_tag_name=target_name,
            target_tag_name=source_name,
            weight=weight
        )
        db.session.add(relationship1)
        db.session.add(relationship2)
    
    # Commit all changes
    db.session.commit()

def create_establishments():
    """Create test establishments with tags."""
    establishments = [
        {
            "name": "Cozy Coffee Corner",
            "description": "A warm and inviting coffee shop perfect for relaxation",
            "tags": [
                ("Cozy", 3),
                ("Relaxed", 2),
                ("Peaceful", 2),
                ("Creative", 1)
            ]
        },
        {
            "name": "The Party Hub",
            "description": "High-energy nightclub for party lovers",
            "tags": [
                ("Party", 3),
                ("Energetic", 3),
                ("Social", 2),
                ("Excited", 2)
            ]
        },
        {
            "name": "Elegant Dining",
            "description": "Fine dining restaurant with romantic atmosphere",
            "tags": [
                ("Elegant", 3),
                ("Romantic", 3),
                ("Intimate", 2),
                ("Traditional", 1)
            ]
        },
        {
            "name": "Modern Workspace",
            "description": "Contemporary coworking space for professionals",
            "tags": [
                ("Modern", 3),
                ("Focused", 3),
                ("Productive", 2),
                ("Networking", 2)
            ]
        }
    ]
    
    for est_data in establishments:
        # Create establishment
        establishment = EstablishmentModel(
            name=est_data["name"],
            description=est_data["description"]
        )
        db.session.add(establishment)
        db.session.flush()  # Get the ID
        
        # Add tags
        for tag_name, count in est_data["tags"]:
            tag_rel = EstablishmentTagModel(
                establishment_id=establishment.id,
                tag_name=tag_name,
                count=count
            )
            db.session.add(tag_rel)
    
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        # Create test data
        create_tags()
        create_establishments() 