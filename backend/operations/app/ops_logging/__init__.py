import os
import logging
from distutils.util import strtobool


def get_log_level():
    if bool(strtobool(os.getenv('DEV_MODE', 'false'))):
        return logging.DEBUG
    else:
        return logging.INFO

logger = logging.getLogger('ops_logger')


logging.basicConfig(
    level=get_log_level(),
    format='[%(asctime)s] %(levelname)-8s| %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )
