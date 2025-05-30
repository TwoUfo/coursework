from flask import request
from flask_restx import Resource, Namespace, fields

from adapters.input.api.schemas import create_establishment_schemas
from adapters.input.api.auth.security import login_required, admin_required
from domain.ports.input.establishment_service import EstablishmentServicePort
from domain.services.establishment_service import EstablishmentService

api = Namespace("establishments", description="Establishment operations")
schemas = create_establishment_schemas(api)

tag_model = api.model(
    "Tag",
    {
        "tag_name": fields.String(required=True, description="Tag name"),
        "count": fields.Integer(required=True, description="Tag count"),
    },
)

comment_model = api.model(
    "Comment",
    {
        "id": fields.Integer(readonly=True),
        "establishment_id": fields.Integer(readonly=True),
        "text": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "created_at": fields.DateTime(readonly=True),
    },
)

establishment_model = api.model(
    "Establishment",
    {
        "id": fields.Integer(required=True, description="Establishment ID"),
        "name": fields.String(required=True, description="Establishment name"),
        "description": fields.String(
            required=True, description="Establishment description"
        ),
        "tags": fields.List(
            fields.Nested(tag_model), required=True, description="Establishment tags"
        ),
        "comments": fields.List(
            fields.Nested(comment_model), description="Establishment comments"
        ),
        "score": fields.Float(description="Search relevance score"),
    },
)

establishment_create_model = api.model(
    "EstablishmentCreate",
    {
        "name": fields.String(required=True, description="Establishment name"),
        "description": fields.String(
            required=False, description="Establishment description"
        ),
    },
)

add_tag_model = api.model(
    "AddTag",
    {"tag_name": fields.String(required=True, description="Name of the tag to add")},
)

success_response = api.model(
    "SuccessResponse",
    {
        "message": fields.String(required=True, description="Success message"),
        "establishment": fields.Nested(
            establishment_model, required=True, description="Updated establishment"
        ),
    },
)

search_request = api.model(
    "SearchRequest",
    {
        "tag_names": fields.List(
            fields.String, required=True, description="List of tag names to search for"
        ),
        "limit": fields.Integer(
            required=False,
            default=10,
            description="Maximum number of results to return",
        ),
    },
)

establishment_tag_model = api.model(
    "EstablishmentTag",
    {
        "tag_name": fields.String(required=True),
        "count": fields.Integer(required=True),
    },
)

comment_input_model = api.model(
    "CommentInput",
    {
        "text": fields.String(required=True, description="Comment text"),
        "rating": fields.Integer(required=True, min=1, max=10, description="Rating from 1 to 10"),
    },
)

_service = None


def init_api(establishment_service: EstablishmentService):
    """Initialize the API with required services."""
    global _service
    _service = establishment_service


@api.route("")
class EstablishmentList(Resource):
    @api.expect(establishment_create_model)
    @api.marshal_with(establishment_model)
    @admin_required
    def post(self):
        """Create a new establishment. Admin only."""
        data = request.json
        establishment = _service.create_establishment(
            {"name": data["name"], "description": data.get("description", "")}
        )
        return establishment

    @api.marshal_list_with(establishment_model)
    @login_required
    def get(self):
        """Get all establishments. Requires authentication."""
        return _service.get_all_establishments()


@api.route("/<int:id>")
class EstablishmentResource(Resource):
    @api.marshal_with(establishment_model)
    @login_required
    def get(self, id):
        """Get an establishment by ID. Requires authentication."""
        establishment = _service.get_establishment(id)
        return establishment


@api.route("/<int:id>/tags")
class EstablishmentTags(Resource):
    @api.expect(add_tag_model)
    @api.marshal_with(success_response)
    @admin_required
    def post(self, id):
        """Add a tag to an establishment. Admin only."""
        data = request.json
        _service.add_tag_to_establishment(
            establishment_id=id, tag_name=data["tag_name"]
        )
        # Return success message with updated establishment
        return {
            "message": f"Tag '{data['tag_name']}' successfully added to establishment",
            "establishment": _service.get_establishment(id),
        }


@api.route("/search")
class EstablishmentSearch(Resource):
    @api.expect(search_request)
    @api.marshal_list_with(establishment_model)
    @login_required
    def post(self):
        """Search establishments by tags. Requires authentication."""
        data = request.json
        tag_names = data.get("tag_names", [])
        limit = data.get("limit", 10)

        tag_weights = {tag_name: 1.0 for tag_name in tag_names}

        establishments = _service.search_establishments(tag_weights, limit)
        return establishments


@api.route("/<int:id>/comments")
class EstablishmentComments(Resource):
    """Endpoint for managing establishment comments."""

    @api.expect(comment_input_model)
    @api.marshal_with(comment_model)
    def post(self, id):
        """Add a comment to an establishment."""
        data = api.payload
        return _service.add_comment(id, data["text"], data["rating"])
