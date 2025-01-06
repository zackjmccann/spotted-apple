import os

SECRET_KEY = os.getenv('SECRET_KEY')
SERVER_NAME = os.getenv('SERVER_NAME')

DEBUG_MODE = os.getenv('DEBUG_MODE', 'false')

if DEBUG_MODE.lower() == 'true':
    FLASK_DEBUG = True
else:
    FLASK_DEBUG = False