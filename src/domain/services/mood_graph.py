from typing import List, Dict
from domain.models.tag import TagRelationship


class MoodGraph:
    """Implementation of mood relationship graph using Floyd-Warshall algorithm."""
    
    def __init__(self, relationships: List[TagRelationship]):
        self.graph = self._build_graph(relationships)
        self._compute_transitive_relationships()
    
    def _build_graph(self, relationships: List[TagRelationship]) -> Dict[str, Dict[str, float]]:
        """Build initial graph from relationships."""
        graph: Dict[str, Dict[str, float]] = {}
        
        # Initialize graph with direct relationships
        for rel in relationships:
            # Initialize source if not exists
            if rel.source_tag_name not in graph:
                graph[rel.source_tag_name] = {}
            
            # Initialize target if not exists
            if rel.target_tag_name not in graph:
                graph[rel.target_tag_name] = {}
            
            # Add relationship weight
            graph[rel.source_tag_name][rel.target_tag_name] = rel.weight
        
        return graph
    
    def _compute_transitive_relationships(self) -> None:
        """
        Compute transitive relationships using Floyd-Warshall algorithm.
        This will find the strongest path between any two moods.
        """
        nodes = list(self.graph.keys())
        
        # Initialize missing relationships with 0 (no relationship)
        for k in nodes:
            for i in nodes:
                if i not in self.graph:
                    self.graph[i] = {}
                for j in nodes:
                    if j not in self.graph[i]:
                        self.graph[i][j] = 0
        
        # Floyd-Warshall algorithm
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    # The strength of a path is the product of its edge weights
                    path_strength = self.graph[i][k] * self.graph[k][j]
                    if path_strength > self.graph[i][j]:
                        self.graph[i][j] = path_strength
    
    def get_all_relationships(self) -> Dict[str, Dict[str, float]]:
        """Get all mood relationships."""
        return self.graph

    def get_related_moods(self, mood_id: str, min_weight: float = 0.1) -> Dict[str, float]:
        """
        Get all moods related to the given mood with weights above the minimum threshold.
        
        Args:
            mood_id: ID of the mood to find relationships for
            min_weight: Minimum weight threshold (default 0.1)
            
        Returns:
            Dictionary mapping related mood IDs to their relationship weights
        """
        if mood_id not in self.graph:
            return {}
        
        return {
            target_id: weight
            for target_id, weight in self.graph[mood_id].items()
            if weight >= min_weight
        } 