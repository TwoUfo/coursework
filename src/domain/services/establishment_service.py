from typing import List, Dict, Optional

from domain.models.establishment import Establishment, EstablishmentTag
from domain.ports.input.establishment_service import EstablishmentServicePort
from domain.ports.output.establishment_repository import EstablishmentRepositoryPort
from domain.ports.input.tag_service import TagServicePort


class EstablishmentService(EstablishmentServicePort):
    """Service for managing establishments."""
    
    def __init__(
        self,
        establishment_repository: EstablishmentRepositoryPort,
        tag_service: TagServicePort
    ):
        self.establishment_repository = establishment_repository
        self.tag_service = tag_service
    
    def create_establishment(self, data: Dict) -> Establishment:
        """Create a new establishment."""
        establishment = Establishment(
            id=None,
            name=data["name"],
            description=data.get("description", ""),
            tags=[]
        )
        return self.establishment_repository.save(establishment)
    
    def get_establishment(self, establishment_id: int) -> Optional[Establishment]:
        """Get an establishment by ID."""
        return self.establishment_repository.get_by_id(establishment_id)
    
    def add_tag_to_establishment(self, establishment_id: int, tag_name: str) -> EstablishmentTag:
        """Add a tag to an establishment."""
        return self.establishment_repository.add_tag(establishment_id, tag_name)
    
    def search_establishments(self, tag_weights: Dict[str, float], limit: int = 10) -> List[Establishment]:
        """Search establishments by tags and their weights."""
        if not tag_weights:
            raise ValueError("At least one tag must be provided")
        
        return self.establishment_repository.get_by_tags(tag_weights, limit)
    
    def search_by_moods(self, tag_names: List[str], limit: int = 10) -> List[Establishment]:
        """Search establishments by mood tags, using the mood graph for related moods."""
        # Get mood graph with relationships
        mood_graph = self.tag_service.get_mood_graph()
        
        # Calculate combined weights for all related tags
        tag_weights: Dict[str, float] = {}
        
        for tag_name in tag_names:
            # Add the direct tag with weight 1.0
            tag_weights[tag_name] = 1.0
            
            # Add related tags with their computed weights
            if tag_name in mood_graph:
                for related_name, weight in mood_graph[tag_name].items():
                    if related_name not in tag_weights or weight > tag_weights[related_name]:
                        tag_weights[related_name] = weight
        
        return self.establishment_repository.get_by_tags(tag_weights, limit) 