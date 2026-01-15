import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    APP_NAME = "S2O Backend"
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    SWAGGER = {
        "title": "S2O API",
        "uiversion": 3
    }


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config():
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
