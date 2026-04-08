from flask_jwt_extended import create_access_token
from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, make_response
from models.user import User
from repositories.auth_repository import auth_repository_instance
from request_models.login_request import LoginRequest
from request_models.register_request import RegisterRequest
from response_models.common_responses import ErrorResponse
from response_models.login_response import LoginResponse
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
def register(body: RegisterRequest) -> RegisterResponse:
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

@auth_bp.post(
    "/login",
    tags=[auth_tag],
    summary="Login to an existing account. Returns JWT on success.",
    responses={
        "201": LoginResponse,
        "401": ErrorResponse,
        "500": ErrorResponse
    }
)
def login(body: LoginRequest) -> LoginResponse:
    try: 
        user: User = auth_repository_instance.login_user(body.name, body.password)
        print(f'user: ',user)
        token = create_access_token(identity=user.id)
        print(f'token: ',token)
        resp = LoginResponse(jwt_token=token)
        return make_response(jsonify(resp.model_dump()), 201)
    except ValueError as vr:
        er: ErrorResponse = ErrorResponse(ErrorMessage=str(vr))
        return make_response(jsonify(er.model_dump()), 401)
    except Exception as e:
        er: ErrorResponse = ErrorResponse(ErrorMessage=str(e))
        return make_response(jsonify(er.model_dump()), 500)
