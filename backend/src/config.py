import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    APP_NAME = "S2O Backend"
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    # ======================
    # DATABASE CONFIG
    # ======================
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/s2o_db"
    )

    SQL_ECHO = False

    # ======================
    # SWAGGER CONFIG
    # ======================
    SWAGGER = {
        "title": "S2O API",
        "uiversion": 3
    }


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQL_ECHO = True   # 👉 dev thì bật log SQL


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQL_ECHO = False


def get_config():
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
