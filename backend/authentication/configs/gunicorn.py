import os
import json
import logging.config
import multiprocessing

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2))
threads = int(os.getenv('PYTHON_MAX_THREADS', 1))
timeout = int(os.getenv('WEB_TIMEOUT', 120))

def process_json_template(value):
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
        return os.getenv(env_var, f"<{env_var} not set>")
    elif isinstance(value, dict):
        return {k: process_json_template(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [process_json_template(item) for item in value]
    else:
        return value

def on_starting(server):
    logging_config_path = os.getenv('LOGGER_CONFIG')

    debug_mode = os.getenv('DEBUG_MODE', 'false')
    if debug_mode.lower() == 'true':
        os.environ['LOG_LEVEL'] = 'DEBUG'
    else:
        os.environ['LOG_LEVEL'] = 'INFO'

    with open(logging_config_path, 'r') as f:
        logging_config_template = json.load(f)
        logging_config = process_json_template(logging_config_template)
        logging.config.dictConfig(logging_config)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    gunicorn_access_logger = logging.getLogger('gunicorn.access')

    server.log.error_log = gunicorn_error_logger
    server.log.access_log = gunicorn_access_logger

    