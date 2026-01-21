from .database_postgres import PostgresDatabase
from .redis_client import RedisClient


def init_db(app):
	"""Initialize database and related clients for the Flask app."""
	# Initialize Postgres (SQLAlchemy engine & session)
	PostgresDatabase.init_app(app)

	# Create tables if configured to do so (useful for local/dev)
	try:
		PostgresDatabase.create_all()
		app.logger.info("Database tables created/verified")
	except Exception as e:
		app.logger.warning(f"Could not auto-create tables: {e}")

	# Initialize Redis client (optional)
	try:
		RedisClient.init_app(app)
		app.logger.info("Redis client initialized")
	except Exception as e:
		app.logger.warning(f"Redis initialization skipped or failed: {e}")


def get_session():
	"""Get a DB session from the configured database backend."""
	return PostgresDatabase.get_session()

