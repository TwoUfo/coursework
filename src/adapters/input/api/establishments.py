from flask import request
from flask_restx import Resource, Namespace, fields

from adapters.input.api.schemas import create_establishment_schemas
from domain.ports.input.establishment_service import EstablishmentServicePort

# Create namespace
api = Namespace("establishments", description="Establishment operations")
schemas = create_establishment_schemas(api)

# Models
tag_model = api.model("Tag", {
    "tag_name": fields.String(required=True, description="Tag name"),
    "count": fields.Integer(required=True, description="Tag count")
})

establishment_model = api.model("Establishment", {
    "id": fields.Integer(required=True, description="Establishment ID"),
    "name": fields.String(required=True, description="Establishment name"),
    "description": fields.String(required=True, description="Establishment description"),
    "tags": fields.List(fields.Nested(tag_model), required=True, description="Establishment tags"),
    "score": fields.Float(description="Search relevance score")
})

establishment_create_model = api.model("EstablishmentCreate", {
    "name": fields.String(required=True, description="Establishment name"),
    "description": fields.String(required=False, description="Establishment description")
})

add_tag_model = api.model("AddTag", {
    "tag_name": fields.String(required=True, description="Name of the tag to add")
})

success_response = api.model("SuccessResponse", {
    "message": fields.String(required=True, description="Success message"),
    "establishment": fields.Nested(establishment_model, required=True, description="Updated establishment")
})

search_request = api.model("SearchRequest", {
    "tag_names": fields.List(fields.String, required=True, description="List of tag names to search for"),
    "limit": fields.Integer(required=False, default=10, description="Maximum number of results to return")
})

# Store service instance
establishment_service = None

def init_api(service):
    """Initialize API with dependencies."""
    global establishment_service
    establishment_service = service

@api.route("")
class EstablishmentList(Resource):
    @api.expect(establishment_create_model)
    @api.marshal_with(establishment_model)
    def post(self):
        """Create a new establishment."""
        data = request.json
        establishment = establishment_service.create_establishment({
            "name": data["name"],
            "description": data.get("description", "")
        })
        return establishment

@api.route("/<int:id>")
class EstablishmentResource(Resource):
    @api.marshal_with(establishment_model)
    def get(self, id):
        """Get an establishment by ID."""
        establishment = establishment_service.get_establishment(id)
        return establishment

@api.route("/<int:id>/tags")
class EstablishmentTags(Resource):
    @api.expect(add_tag_model)
    @api.marshal_with(success_response)
    def post(self, id):
        """Add a tag to an establishment."""
        data = request.json
        establishment_service.add_tag_to_establishment(
            establishment_id=id,
            tag_name=data["tag_name"]
        )
        # Return success message with updated establishment
        return {
            "message": f"Tag '{data['tag_name']}' successfully added to establishment",
            "establishment": establishment_service.get_establishment(id)
        }

@api.route("/search")
class EstablishmentSearch(Resource):
    @api.expect(search_request)
    @api.marshal_list_with(establishment_model)
    def post(self):
        """Search establishments by tags."""
        data = request.json
        tag_names = data.get("tag_names", [])
        limit = data.get("limit", 10)
        
        # Create a dictionary of tag weights (all equal for now)
        tag_weights = {tag_name: 1.0 for tag_name in tag_names}
        
        establishments = establishment_service.search_establishments(tag_weights, limit)
        return establishments 