import os
import pytest
from app.services.errors import TokenError

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
        'iss': 'spotted-apple-auth-service',
        'jti': expected_jti,
        'aud': [good_token_data['aud']]
        })
    
    assert good_token_data == token_data

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

def test_token_service_revoke_token(token_service, good_token_data):
    token = token_service.issue_token(
        aud=good_token_data['aud'],
        iat=good_token_data['iat'],
        exp=good_token_data['exp'],
        context=good_token_data['context'],
        )

    assert token_service.revoke_token(token)

def test_token_service_fail_refresh_of_bad_token(token_service):
    with pytest.raises(TokenError):
        token_service.refresh_access('bad_token')

def test_token_service_fail_refresh_of_blacklist_token(token_service, good_token_data):
    token = token_service.issue_token(
        aud=good_token_data['aud'],
        iat=good_token_data['iat'],
        exp=good_token_data['exp'],
        context=good_token_data['context'],
        )

    assert token_service.revoke_token(token)
    with pytest.raises(TokenError):
        token_service.refresh_access(token)

def test_token_service_refresh_access(token_service, good_token_data):
    # Get Token
    good_token_data.update({
        'context': {
            'id': os.environ['TEST_CLIENT_ID'],
            'roles':['user'],
            'user': os.environ['TEST_USER_EMAIL'],
            }
        })
    token = token_service.issue_token(
        aud=good_token_data['aud'],
        iat=good_token_data['iat'],
        exp=good_token_data['exp'],
        context=good_token_data['context'],
        )
    
    # Refresh Access
    tokens = token_service.refresh_access(token)

    # Verify the token was revoked
    assert not token_service.validate_token(token)

    # Verify the token data is the same as the original token
    token_data = token_service.decode_token(tokens.get('access'))
    expected_jti = f'{os.environ["ID"]}-{os.environ["TEST_CLIENT_ID"]}'

    good_token_data.update({
        'iss': 'spotted-apple-auth-service',
        'jti': expected_jti,
        'aud': [good_token_data['aud']]
        })
    
    del good_token_data['iat']
    del good_token_data['exp']
    del token_data['iat']
    del token_data['exp']
    assert good_token_data == token_data

    # Revoke newly created Tokens
    for token in tokens.values():
        valid = token_service.validate_token(token)

        if valid:
            revoked = token_service.revoke_token(token)
            assert revoked
