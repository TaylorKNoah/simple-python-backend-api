from flask_openapi3 import OpenAPI
from controllers.auth_controller import auth_bp

def register_blueprints(app: OpenAPI) -> None:
    app.register_api(auth_bp)