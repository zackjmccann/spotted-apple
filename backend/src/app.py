import os
# from config.sa_logger import logger
from flask import Flask
from src import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object("config.settings")
    else:
        app.config.from_object('config.flask_testing', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        # logger.debug('Instance file exists')

    @app.route("/hello")
    def hello():
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        conn.commit()
        result = cursor.fetchone()
        cursor.close()

        return f"Hello here is your result {result}!"

    @app.errorhandler(500)
    def server_error(e):
        return "An internal error occurred.", 500

    db.init_app(app)

    return app
