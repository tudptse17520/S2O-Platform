from .database_postgres import PostgresDatabase


def init_db(app):
	"""Initialize database for the Flask app."""
	# Initialize Postgres (SQLAlchemy engine & session)
	PostgresDatabase.init_app(app)

	# Create tables if configured to do so (useful for local/dev)
	try:
		PostgresDatabase.create_all()
		app.logger.info("Database tables created/verified")
	except Exception as e:
		app.logger.warning(f"Could not auto-create tables: {e}")

	# Note: Redis/Cache is initialized separately via cache_service
	# See infrastructure/services/cache_service.py


def get_session():
	"""Get a DB session from the configured database backend."""
	return PostgresDatabase.get_session()
