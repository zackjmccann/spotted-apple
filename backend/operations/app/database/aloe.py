"""
A class representing an instance of the Spotted Apple Database "Aloe"
"""
from psycopg2 import Error
from app.database.postgres import Postgres
from ops_logging import logger


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

    def create_session(self, client_id: str) -> dict:
        query_data = {
            'text': 'SELECT * FROM create_client_app_session(%(client_id)s);',
            'values': {'client_id': client_id}
        }
        return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')

    def revoke_session(self, session_id: str) -> dict:
        query_data = {
            'text': 'SELECT * FROM revoke_client_app_session(%(session_id)s) AS revoked;',
            'values': {'session_id': session_id}
        }
        try:
            return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')
        except Error as err:
            logger.error(f'An error occurred at the database: {err}')
            return False

    def validate_session(self, session_id) -> dict:
        query_data = {
            'text': 'SELECT * FROM validate_client_session(%(session_id)s) AS valid;',
            'values': {'session_id': session_id}
        }
        try:
            return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')
        except Error as err:
            logger.error(f'An error occurred at the database: {err}')
            return False

    def get_session_state(self, session_id) -> dict:
        query_data = {
            'text': 'SELECT * FROM get_client_session_state(%(session_id)s) AS session_state;',
            'values': {'session_id': session_id}
        }
        try:
            return self.execute_query(
            query_data=query_data,
            return_method='fetchone',
            cursor_type='RealDictCursor')
        except Error as err:
            logger.error(f'An error occurred at the database: {err}')
            return False
