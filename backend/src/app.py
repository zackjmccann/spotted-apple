import os
from flask import Flask, jsonify
from database.aloe import init_app
from middleware import Authenticator, routes
from users.routes import users_blueprint
from api.routes import api_blueprint
from spotted_apple_logging import logger


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object("config.settings")
    else:
        app.config.from_object('config.flask_testing', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        logger.debug('Instance file exists')

    @app.route("/")
    def main():
        data = {
            'status': 'success',
            'message': 'Spotted Apple Backend',
        }
        return jsonify(data), 201

    @app.errorhandler(500)
    def server_error(e):
        return "An internal error occurred.", 500

    init_app(app)
    app.wsgi_app = Authenticator(app.wsgi_app)
    app.register_blueprint(routes.auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    return app
