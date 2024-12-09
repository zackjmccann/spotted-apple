"""
A class representing an instance of the Spotted Apple Database "Aloe"
"""
from app.database.postgres import Postgres


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

    def get_user_email(self, email) -> dict:
        query_data = {
            'text': f'SELECT email '
                    f'FROM users WHERE email = %(email)s;',
            'values': {'email': email}
        }

        result = self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')
        
        if not result:
            return {}
        
        return result

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

    def authenticate_client(self, client_credentials):
        query_data = {
            'text': f'SELECT TRUE     AS valid, '
                    f'       username AS username, '
                    f'       id       AS id '
                    f'FROM clients '
                    f'WHERE username = %(username)s '
                    f'AND password = %(password)s '
                    f'AND id = %(id)s;',
            'values': {
                'username': client_credentials['username'],
                'password': client_credentials['password'],
                'id': client_credentials['id'],
                }
        }
        result = self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

        if result is None:
            result = {'valid': False}

        return result
