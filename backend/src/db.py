from src.database.postgres import Postgres
from flask import current_app, g
# from config.sa_logger import logger


def get_db():
    if 'db' not in g:
        db = Postgres()
    return db.get_connection()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
