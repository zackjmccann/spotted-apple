import os
import sys
import logging
from distutils.util import strtobool

def get_log_level():
    if bool(strtobool(os.getenv('DEV_MODE', 'false'))):
        return logging.DEBUG
    else:
        return logging.INFO


logger = logging.getLogger('spotted_apple_logger')

logging.basicConfig(
    level=get_log_level(),
    format='[%(asctime)s] %(levelname)s | %(message)s (%(funcName)s:%(lineno)d)',
    datefmt='%Y-%m-%d %H:%M:%S')
