import logging
import services
import database as db
from flask import Flask
from flask_cors import CORS
from routes import blueprints
from middleware import Middleware

logger = logging.getLogger('default')

def register_extensions(app: Flask):
    db.init_app(app)
    services.init_app(app)

def register_blueprints(app: Flask):
    DEFAULT_CORS_CONFIG = {
        r'/*': {
            'methods': ['POST'],
            'allow_headers': ["Authorization", "Content-Type"],
            'supports_credentials': True,
            },
        }
    
    for blueprint in blueprints:    
        # CORS(blueprint['blueprint'], resources=blueprint.get('cors_config', DEFAULT_CORS_CONFIG))
        app.register_blueprint(blueprint['blueprint'], url_prefix=blueprint['url_prefix'])

def create_app(config: str = 'configs.settings', env: str = 'development'):
    logger.info('Creating Flask app...')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_pyfile(f'{env}.py', silent=True)

    app.wsgi_app = Middleware(app.wsgi_app)

    register_extensions(app)
    register_blueprints(app)

    return app
