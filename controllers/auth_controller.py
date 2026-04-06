from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, make_response
from models.user import User
from repositories.auth_repository import auth_repository_instance
from request_models.register_request import RegisterRequest
from response_models.common_responses import ErrorResponse
from response_models.register_response import RegisterResponse

auth_bp = APIBlueprint("auth", __name__, url_prefix="/auth")
auth_tag = Tag(name="Auth", description="Authentication endpoints")

@auth_bp.post(
    "/register",
    tags=[auth_tag],
    summary="Create a new user account.",
    responses={
        "201": RegisterResponse,
        "409": ErrorResponse,
        "500": ErrorResponse
    }
)
def register(body: RegisterRequest):
    try:
        user: User = auth_repository_instance.register_user(body)
        reg_resp: RegisterResponse = RegisterResponse(id=user.id, name=user.name)
        return make_response(jsonify(reg_resp.model_dump()), 201)
    except ValueError as e:
        er: ErrorResponse = ErrorResponse(ErrorMessage=str(e))
        return make_response(jsonify(er.model_dump()), 409)
    except Exception as e:
        er: ErrorResponse = ErrorResponse(ErrorMessage=str(e))
        return make_response(er.model_dump(), 500)