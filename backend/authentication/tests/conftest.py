import os
import datetime
import pytest
from app.services import TokenService
from app import create_app


@pytest.fixture()
def good_client_headers():
    return {
        'Client-ID': os.environ['TEST_CLIENT_ID'],
        'Client-Name': os.environ['TEST_CLIENT_NAME'],
        'Client-Secret': os.environ['TEST_CLIENT_SECRET'],
        }

@pytest.fixture()
def bad_client_headers():
    return {
        'Client-ID': 'bad_id',
        'Client-Name': os.environ['TEST_CLIENT_NAME'],
        'Client-Secret': os.environ['TEST_CLIENT_SECRET'],
        }

@pytest.fixture(scope='module')
def bad_user():
    return {
        'client_id': os.environ['TEST_CLIENT_ID'],
        'client_name': os.environ['TEST_CLIENT_NAME'],
        'client_secret': os.environ['TEST_CLIENT_SECRET'],
        'grant_type': 'authorization',
        'email': 'bad@user.com',
        'password': 'badp@55w0rd!',
        }

@pytest.fixture(scope='module')
def good_user():
    return {
        'client_id': os.environ['TEST_CLIENT_ID'],
        'client_name': os.environ['TEST_CLIENT_NAME'],
        'client_secret': os.environ['TEST_CLIENT_SECRET'],
        'grant_type': 'authorization',
        'email': os.environ['TEST_USER_EMAIL'],
        'password': os.environ['TEST_USER_PASSWORD'],
        }

@pytest.fixture()
def bad_token_data():
    return {
        'aud': 'not-granted-app',
        'iat': None,
        'exp': None,
        'context': 'test',
    }

@pytest.fixture()
def good_token_data():
    iat = datetime.datetime.now(datetime.timezone.utc).timestamp()
    exp = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)).timestamp()
    return {
        'aud': os.environ['TEST_CLIENT_NAME'],
        'iat': iat,
        'exp': exp,
        'context': {
            'id': os.environ['TEST_CLIENT_ID'],
            'roles':['test']
            }
    }


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({ "TESTING": True, })

    yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def token_service(app):
    """
    Tokens issues by unit test /token routes.

    Unit tests should include revocations, which are checked in the clean up/post yield.
    If tokens are still valid, they are revoked here.
    """
    with app.app_context():
        yield app.token_service

@pytest.fixture(scope='module')
def tokens(app, good_user):
    """
    Tokens issues by unit test /token routes.

    Unit tests should include revocations, which are checked in the clean up/post yield.
    If tokens are still valid, they are revoked here.
    """
    with app.app_context():
        tokens = app.token_service.issue_user_access_tokens(good_user)
        yield tokens

        for token in tokens.values():
            valid = app.token_service.validate_token(token)

            if valid:
                revoked = app.token_service.revoke_token(token)
                assert revoked
