import os
import pytest
from app.services import AuthenticationError


def test_auth_service_fail_to_authenticate_client(auth_service, bad_client_payload):
    with pytest.raises(AuthenticationError):
        response = auth_service.authenticate_client(
            bad_client_payload)

def test_auth_service_authenticate_client(auth_service, good_client_payload):
    response = auth_service.authenticate_client(
            good_client_payload)
    assert response

def test_auth_service_authenticate_user(auth_service, token_service, session_service, token, good_user_payload):
    token_data = token_service.decode_token(token)
    session_id = token_data['context'].get('id', None)
    session_state = session_service.get_session_state(session_id)
    good_user_payload.update({'state': session_state})
    auth_data = auth_service.authenticate_user_account(good_user_payload)
    assert auth_data.get('code', None)

def test_auth_service_failed_to_authenticate_user(auth_service, token_service, session_service, token, bad_user_payload):
    token_data = token_service.decode_token(token)
    session_id = token_data['context'].get('id', None)
    session_state = session_service.get_session_state(session_id)
    bad_user_payload.update({'state': session_state})

    with pytest.raises(AuthenticationError):
        auth_data = auth_service.authenticate_user_account(bad_user_payload)

@pytest.fixture()
def auth_code(auth_service, token_service, session_service, token, good_user_payload):
    token_data = token_service.decode_token(token)
    session_id = token_data['context'].get('id', None)
    session_state = session_service.get_session_state(session_id)
    good_user_payload.update({'state': session_state})
    auth_data = auth_service.authenticate_user_account(good_user_payload)
    yield auth_data.get('code')

def test_auth_service_exchange_authentication_code(auth_service, token_service, session_service, token, auth_code):
    token_data = token_service.decode_token(token)
    session_id = token_data['context'].get('id', None)
    session_state = session_service.get_session_state(session_id)
    payload = {
        'client_id': os.environ['TEST_CLIENT_ID'],
        'client_secret': os.environ['TEST_CLIENT_SECRET'],
        'state': session_state,
        'code': auth_code,
        'grant_type': 'authentication_code'
    }
    tokens = auth_service.exchange_authentication_code(payload)
    assert tokens.get('access_token', None)
