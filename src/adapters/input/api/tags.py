from flask import request
from flask_restx import Resource, Namespace, fields

from adapters.input.api.schemas import create_tag_schemas
from domain.ports.input.tag_service import TagServicePort

# Create namespace
api = Namespace("tags", description="Tag operations")

# Models
tag_model = api.model("Tag", {
    "name": fields.String(required=True, description="Tag name"),
    "description": fields.String(required=True, description="Tag description")
})

tag_relationship_model = api.model("TagRelationship", {
    "source_tag_name": fields.String(required=True, description="Source tag name"),
    "target_tag_name": fields.String(required=True, description="Target tag name"),
    "weight": fields.Float(required=True, description="Relationship weight (0-1)")
})

mood_graph_model = api.model("MoodGraph", {
    "tag_name": fields.String(required=True, description="Tag name"),
    "related_tags": fields.List(fields.Nested(tag_relationship_model), description="Related tags with weights")
})

# Store service instance
tag_service = None

def init_api(service):
    """Initialize API with dependencies."""
    global tag_service
    tag_service = service

@api.route("")
class TagList(Resource):
    @api.marshal_list_with(tag_model)
    def get(self):
        """Get all tags."""
        return tag_service.get_all_tags()
    
    @api.expect(tag_model)
    @api.marshal_with(tag_model)
    def post(self):
        """Create a new tag."""
        data = request.json
        tag = tag_service.create_tag(
            name=data["name"],
            description=data["description"]
        )
        return tag

@api.route("/<string:name>")
class TagResource(Resource):
    @api.marshal_with(tag_model)
    def get(self, name):
        """Get a tag by name."""
        tag = tag_service.get_tag(name)
        return tag
    
    @api.expect(tag_model)
    @api.marshal_with(tag_model)
    def put(self, name):
        """Update a tag."""
        data = request.json
        tag = tag_service.update_tag(
            name=name,
            description=data["description"]
        )
        return tag
    
    def delete(self, name):
        """Delete a tag."""
        tag_service.delete_tag(name)
        return {"message": "Tag deleted successfully"}

@api.route("/relationships")
class TagRelationshipList(Resource):
    @api.expect(tag_relationship_model)
    @api.marshal_with(tag_relationship_model)
    def post(self):
        """Create a new tag relationship."""
        data = request.json
        relationship = tag_service.create_relationship(
            source_tag_name=data["source_tag_name"],
            target_tag_name=data["target_tag_name"],
            weight=data["weight"]
        )
        return relationship

@api.route("/graph")
class MoodGraph(Resource):
    @api.marshal_list_with(mood_graph_model)
    def get(self):
        """Get the complete mood graph."""
        return tag_service.get_mood_graph() 