"""
Class abstraction of a PostgreSQL Database
"""
import os
import logging
import psycopg2
from psycopg2 import Error, extras, pool

logger = logging.getLogger(__name__)

class Postgres:
    def __init__(self):
        self.cluster = os.getenv('CLUSTER_NAME')
        self.client_username = os.getenv('CLIENT_USERNAME')
        self.client_password = os.getenv('CLIENT_PASSWORD')
        self.service_host = os.getenv(f'{self.cluster}_RW_SERVICE_HOST')
        self.service_port = os.getenv(f'{self.cluster}_RW_SERVICE_PORT')
        self.database = os.getenv(f'POSTGRES_DB')
        self.service = f'{self.service_host}:{self.service_port}'
        self.minconn = os.getenv('CONN_POOL_MIN', 1)
        self.maxconn = os.getenv('CONN_POOL_MAX', 5)
        self.connection_string = self._get_connection_string()
        self.pool = self.get_connection_pool()
        logger.info('Connection pool configured')

    def connect(self):
        return psycopg2.connect(dsn=self.connection_string)

    def get_connection_pool(self):
        return pool.SimpleConnectionPool(
            minconn=self.minconn,
            maxconn=self.maxconn,
            dsn=self.connection_string)
        

    def close_connections(self):
        self.pool.closeall()

    def _get_connection_string(self):
        return (f'postgresql://{self.client_username}:{self.client_password}'
                f'@{self.service}/{self.database}')

    def execute_query(self, query_data: dict, return_method: str, cursor_type: str = None):
        conn = self.pool.getconn()

        if cursor_type:
            cursor = conn.cursor(cursor_factory=getattr(extras, cursor_type))
        else:
            cursor = conn.cursor()
        try:
            cursor.execute(query_data['text'], query_data['values'])
            conn.commit()
            result = getattr(cursor, return_method)()
            cursor.close()
            self.pool.putconn(conn)
            return result

        except Error as e:
            cursor.close()
            self.pool.putconn(conn)
            return e
