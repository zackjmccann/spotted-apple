"""
A class representing an instance of the Spotted Apple Database "Aloe"
"""
from auth_logging import logger
from app.database.postgres import Postgres
from psycopg2 import errors


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

    def register_account(self, email: str, password_hash: str, password_salt: str):
        query_data = {
            'text': 'SELECT email, id, created FROM register_account(%(email)s, %(password_hash)s, %(password_salt)s);',
            'values': {
                'email': email,
                'password_hash': password_hash,
                'password_salt': password_salt
            }
        }

        results = self.execute_query(query_data=query_data, return_method='fetchone', cursor_type='RealDictCursor')
        try:
            assert type(results) != errors.UniqueViolation
            return results
        except AssertionError:
            logger.critical('Failed to insert new account info')
            return {'email': None, 'id': -1, 'created': None}

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
