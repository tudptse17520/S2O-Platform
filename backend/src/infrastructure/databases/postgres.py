from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

# Defaut URI if not in env, matching user request
DEFAULT_DB_URI = "postgresql+psycopg2://postgres:1234@localhost:5433/s2o_db"

def get_database_uri():
    return os.getenv("DATABASE_URI", DEFAULT_DB_URI)

engine = create_engine(get_database_uri(), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
