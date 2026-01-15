import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )

    console_handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[file_handler, console_handler]
    )
