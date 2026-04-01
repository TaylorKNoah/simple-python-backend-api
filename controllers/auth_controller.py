from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, make_response
from pydantic import ValidationError
from request_models.register_request import RegisterRequest

auth_bp = APIBlueprint("auth", __name__, url_prefix="/auth")
auth_tag = Tag(name="Auth", description="Authentication endpoints")

@auth_bp.post("/register", tags=[auth_tag], summary="Create a new user account.")
def register(body: RegisterRequest):
    return make_response(jsonify(message="it worked!"), 201)