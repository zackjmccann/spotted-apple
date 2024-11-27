"""
A class representing an instance of the Spotted Apple Database "Aloe"
"""
from flask import g
from src.database.postgres import Postgres


def connect():
    if 'aloe' not in g:
        aloe = Aloe()
    return aloe.get_connection()

def close(e=None):
    aloe = g.pop('aloe', None)
    if aloe is not None:
        aloe.close_connections()

def init_app(app):
    app.teardown_appcontext(close)


class Aloe(Postgres):
    def __init__(self):
        super().__init__()

    def get_user(self, id) -> dict:
        query_data = {
            'text': f'SELECT id, created, email, first_name, last_name '
                    f'FROM users WHERE id = %(id)s;',
            'values': {'id': id}
        }

        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def insert_user(self, user_data: dict) -> int:
        query_data = {
            'text': f'INSERT INTO users (email, first_name, last_name) '
                    f'VALUES (%(email)s, %(first_name)s, %(last_name)s) RETURNING users.id, users.created;',
            'values': user_data
        }

        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def delete_user(self, id: int) -> int:
        query_data = {
            'text': f'DELETE FROM users WHERE id = %(id)s '
                    f'RETURNING users.id;',
            'values': {'id': id}
            }

        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')
