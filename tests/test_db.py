import os
import pytest
import psycopg


@pytest.fixture
def unit_test_user():
    """Fixture used for unit test, and removed along the way"""
    email = 'unit_test_user@email.com'
    password = 'unit_test_password'
    return (email, password)

def test_postgres_query(postgres):
    with postgres.conn.cursor() as cursor:
        cursor.execute('SELECT 1;')
        results = cursor.fetchall()
    postgres.conn.close()
    assert results[0][0] == 1

def test_spotted_apple_db_create_new_user(spotted_apple_db, unit_test_user):
    test_user_id = spotted_apple_db.create_new_user(unit_test_user)
    assert isinstance(test_user_id, int)

def test_spotted_apple_db_create_existing_user(spotted_apple_db, unit_test_user):
    test_user_id = spotted_apple_db.create_new_user(unit_test_user)
    assert isinstance(test_user_id, psycopg.errors.UniqueViolation)

def test_spotted_apple_db_get_user(spotted_apple_db, unit_test_user):
    user_data = spotted_apple_db.get_user(unit_test_user[0])
    assert user_data[1] == unit_test_user[0]

def test_spotted_apple_db_delete_existing_user(spotted_apple_db, unit_test_user):
    test_user_id = spotted_apple_db.delete_user(unit_test_user[0])
    assert test_user_id == unit_test_user[0]

def test_spotted_apple_db_hash_password(spotted_apple_db):
    password_to_hash = 'secret_password_123'
    hashed_password = spotted_apple_db.hash_password(password_to_hash)
    assert isinstance(hashed_password, str)

def test_spotted_apple_db_verify_password(spotted_apple_db):
    password = 'secret_password_123'
    hashed_password = spotted_apple_db.hash_password(password)
    assert spotted_apple_db.verify_password(password, hashed_password)

def test_add_spotify_authorization_data(spotted_apple_db):
    user_id = os.getenv('TEST_USER_ID')
    auth_code = 'test_auth_code'
    refresh_token = 'test_refresh_token'
    returned_refresh_token = spotted_apple_db.add_spotify_authorization_data(
        user_id=user_id,
        auth_code=auth_code,
        refresh_token=refresh_token)
    assert returned_refresh_token == refresh_token
