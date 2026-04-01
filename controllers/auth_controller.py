from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, make_response
from models.user import User
from repositories.auth_repository import auth_repository
from request_models.register_request import RegisterRequest

auth_bp = APIBlueprint("auth", __name__, url_prefix="/auth")
auth_tag = Tag(name="Auth", description="Authentication endpoints")

@auth_bp.post("/register", tags=[auth_tag], summary="Create a new user account.")
def register(body: RegisterRequest):
    try:
        user: User = auth_repository.register_user(body)
        return make_response(jsonify(id=user.id, name=user.name), 201)
    except ValueError as e:
        return make_response(jsonify(error=str(e)), 409)