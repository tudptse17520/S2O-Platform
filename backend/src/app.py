from create_app import create_app
import logging

logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    logger.info("Starting S2O Backend server...")
    app.run(host="0.0.0.0", port=5000, debug=True)

