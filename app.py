import os
from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI, Info
from config.settings import get_config
from startup.register_blueprints import register_blueprints
from startup.extensions import db, migrate

def create_app(config_name="default"):
    print("")
    info = Info(title="Simple Python Flask API", version="1.0.0")
    app = OpenAPI(__name__, info=info)

    app.config.from_object(get_config(config_name))

    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "DEV_JWT_SECRET_KEY"  # fallback for local/dev
    )

    db.init_app(app)
    migrate.init_app(app, db)

    JWTManager(app)

    register_blueprints(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)