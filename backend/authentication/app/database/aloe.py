"""
A class representing an instance of the Spotted Apple Database "Aloe"
"""
from app.database.postgres import Postgres
from psycopg2 import errors

def init_app(app):
    app.logger.debug('Initializing database...')
    app.db = Aloe()


class AloeError(Exception):
    pass


class Aloe(Postgres):
    def __init__(self):
        super().__init__()

    def authenticate_service(self, service_credentials):
        query_data = {
            'text': 'SELECT authenticate_service(%(service_id)s, %(service_name)s, %(service_secret)s) AS valid; ',
            'values': {
                'service_id': service_credentials['service_id'],
                'service_name': service_credentials['service_name'],
                'service_secret': service_credentials['service_secret'],
                }
        }
        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def validate_client(self, client_credentials):
        query_data = {
            'text': 'SELECT validate_client(%(id)s, %(name)s, %(secret)s) AS valid; ',
            'values': {
                'id': client_credentials['client_id'],
                'name': client_credentials['client_name'],
                'secret': client_credentials['client_secret'],
                }
        }
        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

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
            # logger.critical('Failed to insert new account info')
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
            # logging.critical('Failed to create new user')
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

    def blacklist_token(self, token):
        query_data = {
            'text': 'SELECT token FROM blacklist_token(%(token)s);',
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
            raise AloeError('Failed to blacklist token')

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

    def issue_authorization_code(self) -> dict:
        query_data = {
            'text': 'SELECT issue_oauth_authorization_code() AS auth_code;',
            'values': {}
        }
        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def validate_authorization_code(self, auth_code: str) -> dict:
        query_data = {
            'text': 'SELECT * FROM validate_oauth_authorization_code(%(auth_code)s) AS valid;',
            'values': {'auth_code': auth_code}
        }
        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')
