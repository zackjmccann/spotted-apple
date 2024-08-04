import pytest
import psycopg


@pytest.fixture
def test_user():
    email = 'test_user@email.com'
    password = 'test_password'
    return (email, password)

def test_postgres_query(postgres):
    with postgres.conn.cursor() as cursor:
        cursor.execute('SELECT 1;')
        results = cursor.fetchall()
    postgres.conn.close()
    assert results[0][0] == 1

def test_spotted_apple_db_create_new_user(spotted_apple_db, test_user):
    test_user_id = spotted_apple_db.create_new_user(test_user)
    assert isinstance(test_user_id, int)

def test_spotted_apple_db_create_existing_user(spotted_apple_db, test_user):
    test_user_id = spotted_apple_db.create_new_user(test_user)
    assert isinstance(test_user_id, psycopg.errors.UniqueViolation)

def test_spotted_apple_db_delete_existing_user(spotted_apple_db, test_user):
    test_user_id = spotted_apple_db.delete_user(test_user[0])
    assert test_user_id == test_user[0]
