from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ví dụ URL:
# postgresql+psycopg2://username:password@localhost:5432/yourdb

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:123456@localhost:5432/yourdb"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,    # set=False nếu không muốn log query SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency cho FastAPI – cung cấp session cho repository."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
