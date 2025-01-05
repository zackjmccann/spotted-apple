import pytest

@pytest.fixture()
def create_session(client, good_client_payload, good_client_id, token_service, session_service):
    response = client.post(
        '/auth/session/create',
        json=good_client_payload)

    assert response.status_code == 200
    
    data = response.get_json()
    session = data.get('session', None)
    assert session is not None

    yield {
        'session': session,
        'client_id': good_client_id
        }

    token_data = token_service.decode_token(session)
    session_id = token_data['context'].get('id', None)
    revoked = session_service.revoke_session(session_id)
    assert revoked

def test_auth_fail_to_create_session(client, bad_client_payload):
    response = client.post( '/auth/session/create', json=bad_client_payload)
    data = response.get_json()
    assert response.status_code == 400
    assert data.get('message') == 'Unable to create or get session'

def test_auth_session_introspect(client, create_session):
    response = client.post('/auth/session/introspect', json=create_session)
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('valid', False)

def test_auth_session_introspect(client, create_session):
    response = client.post('/auth/session/revoke', json=create_session)
    data = response.get_json()
    assert response.status_code == 200
    assert data.get('revoked', False)
