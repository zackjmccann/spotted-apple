"""
Class abstraction of a PostgreSQL Database
"""
import os
import psycopg2
from psycopg2 import Error

class Postgres:
    def __init__(self, service, namespace, database):
        self.client_username = os.getenv('CLIENTUSERNAME')
        self.client_password = os.getenv('CLIENTPASSWORD')
        self.service = service 
        self.namespace = namespace # 'backend'
        self.database = database # 'sa-staging'
        self.connection_string = self._get_connection_string()

    def get_connection(self):
        return psycopg2.connect(dsn=self.connection_string)

    def _get_connection_string(self):
        return (f'postgresql://{self.client_username}:{self.client_password}'
                f'@{self.service}.{self.namespace}/{self.database}')

    def execute_query(self, query_data: dict):
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query_data['text'])
                conn.commit()
                result = cursor.fetchone()
                cursor.close()
                return result

            except Error as e:
                cursor.close()
                return e
