from flask import Flask

from config.settings import get_config
from .extensions import db, migrate

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)

    import models.user

    return app