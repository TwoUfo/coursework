from flask_restx import fields

def create_tag_schemas(api):
    """Create tag related schemas."""
    return {
        "tag": api.model("Tag", {
            "name": fields.String(required=True, description="Tag name"),
            "description": fields.String(description="Tag description")
        }),
        "tag_relationship": api.model("TagRelationship", {
            "source_tag_name": fields.String(required=True, description="Source tag name"),
            "target_tag_name": fields.String(required=True, description="Target tag name"),
            "weight": fields.Float(required=True, description="Relationship weight (0-1)")
        })
    }

def create_establishment_schemas(api):
    """Create establishment related schemas."""
    return {
        "establishment": api.model("Establishment", {
            "id": fields.Integer(description="Establishment ID"),
            "name": fields.String(required=True, description="Establishment name"),
            "description": fields.String(description="Establishment description"),
            "tags": fields.List(fields.Nested(api.model("EstablishmentTag", {
                "tag_name": fields.String(description="Tag name"),
                "count": fields.Integer(description="Tag count")
            })))
        }),
        "establishment_search": api.model("EstablishmentSearch", {
            "tag_names": fields.List(
                fields.String,
                required=True,
                description="List of tag names to search by"
            ),
            "limit": fields.Integer(
                default=10,
                description="Maximum number of results to return"
            )
        }),
        "add_tag": api.model("AddTag", {
            "tag_name": fields.String(required=True, description="Tag name to add")
        })
    } 