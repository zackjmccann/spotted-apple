import os
import psycopg

class Postgres:
    def __init__(self):
        self.database = os.getenv('POSTGRES_DB')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')
        self.conn = self.get_connection()

    def get_connection(self):
        return psycopg.connect(conninfo=f'postgresql://'
                                        f'{self.user}:{self.password}@'
                                        f'{self.host}:{self.port}'
                                        f'/{self.database}')
