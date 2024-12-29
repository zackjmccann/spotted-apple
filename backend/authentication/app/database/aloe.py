"""
A class representing an instance of the Spotted Apple Database "Aloe"
"""
from auth_logging import logger
from app.database.postgres import Postgres
from psycopg2 import errors


class Aloe(Postgres):
    def __init__(self):
        super().__init__()

    def register_account(self, email: str, password: str):
        query_data = {
            'text': 'SELECT email, id, created FROM register_account(%(email)s, %(password)s);',
            'values': {
                'email': email,
                'password': password,
            }
        }

        results = self.execute_query(query_data=query_data, return_method='fetchone', cursor_type='RealDictCursor')
        try:
            assert type(results) != errors.UniqueViolation
            return results
        except AssertionError:
            logger.critical('Failed to insert new account info')
            return {'email': None, 'id': -1, 'created': None}

    def create_user(self, id: int, email: str, first_name: str, last_name: str):
        query_data = {
            'text': 'SELECT fk_id AS id, email, first_name, last_name, created, modified FROM create_user(%(id)s, %(email)s, %(first_name)s, %(last_name)s);',
            'values': {
                'id': id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        }

        results = self.execute_query(query_data=query_data, return_method='fetchone', cursor_type='RealDictCursor')
        try:
            assert type(results) != errors.UniqueViolation
            return results
        except AssertionError:
            logger.critical('Failed to create new user')
            return {'id': -1, 'email': None, 'created': None}

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

    def authenticate_user(self, user_account_credentials):
        query_data = {
            'text': 'SELECT authenticate_user(%(email)s, %(password)s) AS valid;',
            'values': {
                'email': user_account_credentials['email'],
                'password': user_account_credentials['password'],
                }
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

    def get_user(self, account_id) -> dict:
        query_data = {
            'text': 'SELECT fk_id AS id, email, first_name, last_name, created, modified FROM get_user_account(%(id)s);',
            'values': { 'id': account_id }
        }

        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')
