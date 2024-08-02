import os
import psycopg

class Postgres:
    def __init__(self):
        self.database = os.getenv('POSTGRES_DB')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')
        self.cursor = self._get_cursor()

    def _get_engine(self):
        return psycopg.connect(conninfo=f'postgresql://'
                                        f'{self.user}:{self.password}@'
                                        f'{self.host}:{self.port}'
                                        f'/{self.database}')

    def _get_cursor(self):
        return self._get_engine().cursor()  

    def execute(self, query: str) -> psycopg.Cursor:
        cur = self._get_cursor()
        cur.execute(query)
        
        return cur.fetchall()

    def close(self):
        self.cursor.close()
