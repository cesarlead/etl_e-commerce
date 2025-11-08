# src/logging_config.py
import logging.config
import os
from pathlib import Path


def setup_logging():
    """Configura el sistema de logging para el proyecto."""

    # Asegura que el directorio de logs exista
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "etl_process.log"

    # Configuración del diccionario de logging
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'
            },
            'simple': {
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file,
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {  # Logger raíz
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True
            },
            'pandas': {  # Silencia logs de librerías de terceros si es necesario
                'level': 'WARNING',
                'propagate': True
            },
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)