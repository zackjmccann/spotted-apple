import os
from flask import Flask
from flask_cors import CORS
from database import aloe
from routes import blueprints
from middleware import Authenticator
from utilities import BackendResponse
from auth_logging import logger


def create_app(config='config.settings'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.response_class = BackendResponse

    try:
        os.makedirs(app.instance_path)
    except OSError:
        logger.debug('Instance file exists')

    with app.app_context():
        try:
            aloe.connect()
            aloe.close_connections()
        except Exception as e:
            logger.critical(f'Connection to the database failed: {e}')

    app.wsgi_app = Authenticator(app.wsgi_app)

    for blueprint in blueprints:
        DEFAULT_CORS_CONFIG = {
             r'/*': {
                 'methods': ['GET', 'POST', 'OPTIONS'],
                 'allow_headers': ["Authorization", "Content-Type"],
                 'supports_credentials': True
                 }
        }

        CORS(blueprint['blueprint'], resources=blueprint.get('cors_config', DEFAULT_CORS_CONFIG))
        app.register_blueprint(blueprint['blueprint'], url_prefix=blueprint['url_prefix'])

    return app
