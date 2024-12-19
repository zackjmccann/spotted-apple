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
