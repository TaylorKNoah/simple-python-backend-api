from flask_openapi3 import OpenAPI, Info
from config.settings import get_config
from startup.register_blueprints import register_blueprints
from startup.extensions import db, migrate


def create_app(config_name="default"):
    print("")
    info = Info(title="Simple Python Flask API", version="1.0.0")
    app = OpenAPI(__name__, info=info)
    print(">>> USING OPENAPI APP FACTORY <<<")
    print("APP TYPE:", type(app))
    print("OPENAPI CLASS MODULE:", OpenAPI.__module__)

    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)

    import models.user

    @app.get("/")
    def index():
        return {"message": "API is running"}


    register_blueprints(app)

    return app