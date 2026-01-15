from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .base import Base


class PostgresDatabase:
    _engine = None
    _Session = None

    @classmethod
    def init_app(cls, app):
        database_url = app.config["SQLALCHEMY_DATABASE_URI"]

        cls._engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=app.config.get("SQL_ECHO", False),
        )

        cls._Session = scoped_session(
            sessionmaker(
                bind=cls._engine,
                autocommit=False,
                autoflush=False,
            )
        )

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            cls._Session.remove()

    @classmethod
    def get_session(cls):
        if cls._Session is None:
            raise RuntimeError("PostgresDatabase is not initialized")
        return cls._Session()

    @classmethod
    def create_all(cls):
        Base.metadata.create_all(bind=cls._engine)

