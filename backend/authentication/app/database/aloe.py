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
                    f'FROM account_access_info WHERE id = %(id)s;',
            'values': {'id': id}
        }

        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def get_user_email(self, email) -> dict:
        query_data = {
            'text': f'SELECT email '
                    f'FROM account_access_info WHERE email = %(email)s;',
            'values': {'email': email}
        }

        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

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
            'text': f'DELETE FROM account_access_info WHERE id = %(id)s '
                    f'RETURNING account_access_info.id;',
            'values': {'id': id}
            }

        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def authenticate_client(self, client_credentials):
        query_data = {
            'text': 'SELECT authenticate_client(%(username)s, %(password)s, %(id)s) AS valid; ',
            'values': {
                'username': client_credentials['username'],
                'password': client_credentials['password'],
                'id': client_credentials['id'],
                }
        }
        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def blacklist_token(self, token):
        query_data = {
            'text': 'SELECT id FROM blacklist_token(%(token)s);',
            'values': { 'token': token }
        }
        results = self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

        try:
            assert type(results) != errors.UniqueViolation
            return results
        except AssertionError:
            raise KeyError('Failed to blacklist token')

    def check_token_blacklist(self, token):
        query_data = {
            'text': 'SELECT check_if_token_is_blacklisted(%(token)s) AS token_is_blacklisted;',
            'values': { 'token': token }
        }
        results = self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

        try:
            assert type(results) != errors.UniqueViolation
            return results
        except AssertionError:
            raise KeyError('Failed to blacklist token')
