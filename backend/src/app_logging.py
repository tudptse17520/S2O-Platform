import logging
import logging.config
import os

def setup_logging(app):
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG' if app.debug else 'INFO',
        }
    }
    logging.config.dictConfig(logging_config)
