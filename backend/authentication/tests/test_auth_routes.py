"""Unit tests for endpoints at the /auth route"""


def test_auth_failed_login_missing_client_info(client):
    """
    Fail a login attempt due to a request failing to contain a Client-ID  header.

    The request should not reach the /auth/login endpoint, and should
    be rejected by the middleware.
    """
    headers = { "Not-Client-ID": 'bad_id' }
    response = client.post('/auth/login', headers=headers)
    data = response.get_json()

    assert response.status_code == 500
    message =  data.get('message')
    assert message == 'Bad Request.'

def test_auth_failed_login_bad_client_info(client, bad_client_headers):
    """
    Fail a login attempt due to a request containing bad client info.

    The request should not reach the /auth/login endpoint, and should
    be rejected by the middleware.
    """
    response = client.post('/auth/login', headers=bad_client_headers)
    data = response.get_json()

    assert response.status_code == 400
    message =  data.get('message')
    assert message == 'Unknown client.'

def test_auth_failed_bad_user(client, good_client_headers, bad_user):
    """Fail a login attempt due to bad user credentials."""
    response = client.post('/auth/login', headers=good_client_headers, json=bad_user)
    data = response.get_json()

    assert response.status_code == 400
    message =  data.get('message')
    assert message == 'Failed to authenticate.'

def test_auth_authenticate_user(client, good_client_headers, good_user):
    """Authenticate a user"""
    response = client.post('/auth/login', headers=good_client_headers, json=good_user)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('access')
    assert data.get('refresh')
