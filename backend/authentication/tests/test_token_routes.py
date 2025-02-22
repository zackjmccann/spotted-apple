"""Unit tests for endpoints at the /token route"""

def test_token_introspect_bad_token(client, good_client_headers):
    """
    Verify a token is bad.

    The request should not experience errors, it should successfully handle and process
    the request, but simply responsed with the appropriate "invalid" response.
    """
    payload = {'token': 'bad-token'}
    response = client.post('/token/introspect', headers=good_client_headers, json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert not data.get('valid')

def test_token_introspect_bad_payload(client, good_client_headers, tokens):
    """
    Verify a token payload is bad. The payload should contain a valid token, but
    still reject the request due to improper payload structure.

    The request should not experience errors, it should successfully handle and process
    the request, but simply responsed with the appropriate "invalid" response.
    """
    payload = {'access_token': tokens.get('access')}
    response = client.post('/token/introspect', headers=good_client_headers, json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert not data.get('valid')

def test_token_introspect(client, good_client_headers, tokens):
    """
    Verify a token payload is bad. The payload should contain a valid token, but
    still reject the request due to improper payload structure.

    The request should not experience errors, it should successfully handle and process
    the request, but simply responsed with the appropriate "invalid" response.
    """
    payload = {'token': tokens.get('access')}
    response = client.post('/token/introspect', headers=good_client_headers, json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('valid')

def test_token_revoke(client, good_client_headers, tokens):
    """
    Verify a token has been is revoked via the /token/revoke endpoint.

    The request should not experience errors, it should successfully handle and process
    the request, but simply responsed with the appropriate "invalid" response.
    """
    print(tokens)
    payload = {'token': tokens.get('access')}
    response = client.post('/token/revoke', headers=good_client_headers, json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('revoked')

    payload = {'token': tokens.get('refresh')}
    response = client.post('/token/revoke', headers=good_client_headers, json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('revoked')

def test_token_refresh(client, good_client_headers, refresh_token):
    """Refresh user access"""
    print(f'Test Refresh: {refresh_token}')
    payload = {'token': refresh_token}
    response = client.post('/token/refresh', headers=good_client_headers, json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('access')
    assert data.get('refresh')
