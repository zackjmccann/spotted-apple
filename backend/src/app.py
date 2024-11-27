import os
from flask import Flask, jsonify
from database.aloe import connect, close, init_app
from users.routes import users_blueprint
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
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        conn.commit()
        result = cursor.fetchone()
        cursor.close()

        data = {
            'status': 'success',
            'message': f"Main result {result[0]}!",
        }
        return jsonify(data), 201

    @app.errorhandler(500)
    def server_error(e):
        return "An internal error occurred.", 500

    init_app(app)
    app.register_blueprint(users_blueprint, url_prefix='/users')

    return app
