import os
from dotenv import load_dotenv

load_dotenv()

class DevConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DEV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("DEV_JWT_SECRET_KEY")

def get_config(name: str):
    mapping = {
        "dev": DevConfig,
        "default": DevConfig,
    }

    return mapping.get(name, DevConfig)