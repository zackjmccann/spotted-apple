import os
import datetime
import pytest
from app.services import AuthService, SessionService, TokenService
from app import create_app


@pytest.fixture
def auth_service():
    return AuthService()

@pytest.fixture()
def session_service():
    return SessionService()

@pytest.fixture
def token_service():
    return TokenService()

@pytest.fixture()
def good_client_id():
    return os.environ['TEST_CLIENT_ID']

@pytest.fixture()
def bad_client_id():
    return 1

@pytest.fixture
def good_client_payload():
    return {
        'client_id': os.environ['TEST_CLIENT_ID'],
        'username': os.environ['TEST_CLIENT_USERNAME'],
        'secret': os.environ['TEST_CLIENT_SECRET'],
        'grant_type': 'client_credentials',
    }

@pytest.fixture
def bad_client_payload():
    return {
        'client_id': 'bad-id',
        'username': '--bad username',
        'secret': 'bad secret:',
        'grant_type': 'client_credential',
    }

@pytest.fixture
def good_token_data():
    iat = datetime.datetime.now(datetime.timezone.utc).timestamp()
    exp = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)).timestamp()
    return {
        'aud': os.environ['TEST_CLIENT_ID'],
        'iat': iat,
        'exp': exp,
        'context': {
            'id': os.environ['TEST_CLIENT_ID'],
            'roles':['test']
            }
    }

@pytest.fixture
def bad_token_data():
    return {
        'aud': 'not-granted-app',
        'iat': None,
        'exp': None,
        'context': 'test',
    }

@pytest.fixture()
def session(session_service, good_client_id):
    session = session_service.create_session(good_client_id)
    yield session
    revoked = session_service.revoke_session(session['session_id'])
    assert revoked
    pass

@pytest.fixture
def invalid_session(good_client_id):
    return {
        'id': 1,
        'session_id': 'an-invalid-session',
        'client_id': good_client_id,
        'created_at': datetime.datetime.now().replace(tzinfo=datetime.timezone.utc),
        'expires_at': datetime.datetime.now().replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(minutes=5),
        }

@pytest.fixture()
def token(session_service, token_service, good_client_id):
    session = session_service.create_session(good_client_id)
    session_token = token_service.issue_session_token(session)
    yield session_token
    revoked = session_service.revoke_session(session['session_id'])
    assert revoked
    pass

@pytest.fixture
def good_user_payload():
    return {
        'client_id': os.environ['TEST_CLIENT_ID'],
        'client_secret': os.environ['TEST_CLIENT_SECRET'],
        'email': os.environ['TEST_USER_EMAIL'],
        'password': os.environ['TEST_USER_PASSWORD'],
        'grant_type': 'authorization'
    }

@pytest.fixture
def bad_user_payload(token):
    return {
        'client_id': os.environ['TEST_CLIENT_ID'],
        'client_secret': os.environ['TEST_CLIENT_SECRET'],
        'session': token,
        'email': 'bad@email.com',
        'password': 'wrongPA55word!',
        'grant_type': 'authorization'
    }

@pytest.fixture(scope='module')
def client():
    app = create_app(config={"TESTING": True})
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
