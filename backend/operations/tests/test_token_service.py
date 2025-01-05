import os
import pytest
from app.services import TokenError


def test_token_service_fail_to_issue_token(token_service, bad_token_data):
    with pytest.raises(TokenError):
        response = token_service.issue_token(
            aud=bad_token_data['aud'],
            iat=bad_token_data['iat'],
            exp=bad_token_data['exp'],
            context=bad_token_data['context'],
            )

def test_token_service_issue_token(token_service, good_token_data):
    response = token_service.issue_token(
            aud=good_token_data['aud'],
            iat=good_token_data['iat'],
            exp=good_token_data['exp'],
            context=good_token_data['context'],
            )
    assert type(response) == str

def test_token_service_decode_token(token_service, good_token_data):
    token = token_service.issue_token(
            aud=good_token_data['aud'],
            iat=good_token_data['iat'],
            exp=good_token_data['exp'],
            context=good_token_data['context'],
            )
    token_data = token_service.decode_token(token)
    expected_jti = f'{os.environ["ID"]}-{os.environ["TEST_CLIENT_ID"]}'

    good_token_data.update({
        'iss': 'spotted-apple-ops-backend',
        'jti': expected_jti,
        'aud': [good_token_data['aud']]
        })

    assert token_data == good_token_data

def test_token_service_issue_session_token(token_service, session):
    response = token_service.issue_session_token(session)
    assert type(response) == str

def test_token_service_invalid_token(token_service):
    assert not token_service.validate_token('bad_token')

def test_token_service_validate_token(token_service, good_token_data):
    token = token_service.issue_token(
            aud=good_token_data['aud'],
            iat=good_token_data['iat'],
            exp=good_token_data['exp'],
            context=good_token_data['context'],
            )
    assert token_service.validate_token(token)
