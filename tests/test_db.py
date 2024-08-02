import pytest

def test_postgres_query(postgres_conn):
    results = postgres_conn.execute('SELECT 1;')
    assert results[0][0] == 1
    postgres_conn.close()
