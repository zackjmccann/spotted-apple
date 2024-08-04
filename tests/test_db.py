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

def test_spotted_apple_db_get_user(spotted_apple_db, test_user):
    user_data = spotted_apple_db.get_user(test_user[0])
    assert user_data[1] == test_user[0]

def test_spotted_apple_db_delete_existing_user(spotted_apple_db, test_user):
    test_user_id = spotted_apple_db.delete_user(test_user[0])
    assert test_user_id == test_user[0]

def test_spotted_apple_db_hash_password(spotted_apple_db):
    password_to_hash = 'secret_password_123'
    hashed_password = spotted_apple_db.hash_password(password_to_hash)
    assert isinstance(hashed_password, str)

def test_spotted_apple_db_verify_password(spotted_apple_db):
    password = 'secret_password_123'
    hashed_password = spotted_apple_db.hash_password(password)
    assert spotted_apple_db.verify_password(password, hashed_password)
