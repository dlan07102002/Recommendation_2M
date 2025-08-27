import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    numeric_log_level = getattr(logging, log_level, logging.INFO)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(numeric_log_level)

    # Clear existing handlers to prevent duplicate logs in Flask debug mode
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (for production-like logging)
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=1024 * 1024 * 5,  # 5 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Suppress werkzeug (Flask's development server) logs if not in debug mode
    # This is handled by Flask's app.run(debug=True) which sets up its own logger
    # For production, you'd typically use a WSGI server like Gunicorn/uWSGI
    if os.getenv('FLASK_ENV') != 'development': # Assuming FLASK_ENV is set in production
        logging.getLogger('werkzeug').setLevel(logging.WARNING)

    logger.info(f"Logging configured with level: {log_level}")
