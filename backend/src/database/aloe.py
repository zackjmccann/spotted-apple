"""
A class representing an instance of the Spotted Apple Database, called Aloe
"""
from src.database.postgres import Postgres


class Aloe(Postgres):
    def __init__(self, service, namespace, database):
        super().__init__(service, namespace, database)
        # service='spotted-apple-cnpg-rw'
        # namespace='backend'
        # database='sa-staging'

    def get_user(self, user_data, column: str = 'user_id') -> dict:
        get_user_query_data = {
            'name': f'get-user-{str(user_data)}',
            'text': f"SELECT user_id, email, created "
                    f"FROM users WHERE {column} = $1;",
            'values': [user_data]
            }

        return self.execute_query(get_user_query_data)


    def delete_user(self, user_id: int) -> int:
        delete_user_query_data = {
            'name': f'delete-user={user_id}',
            'text': f"DELETE FROM users WHERE user_id = $1 "
                    f"RETURNING users.user_id;",
            'values': [user_id]
            }

        return self.execute_query(delete_user_query_data)


    def insert_user(self, user_data: dict) -> int:
        insert_user_query_data = {
            'name': f'insert-user-{user_data["email"]}',
            'text': f"INSERT INTO users (email, first_name, last_name) "
                    f"VALUES ($1, $2, $3) RETURNING users.user_id;",
            'values': [
                user_data["email"],
                user_data["first_name"],
                user_data["last_name"]
                ]
        }

        return self.execute_query(insert_user_query_data)
