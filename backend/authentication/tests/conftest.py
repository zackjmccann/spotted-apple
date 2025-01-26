import os
import datetime
import pytest
from app import create_app


@pytest.fixture()
def good_service_payload():
    return {
        'service_id': os.environ['TEST_SERVICE_ID'],
        'service_name': os.environ['TEST_SERVICE_NAME'],
        'service_secret': os.environ['TEST_SERVICE_SECRET'],
        'grant_type': 'client_credentials',
        }

@pytest.fixture()
def bad_service_payload():
    return {
        'service_id': 'bad_id',
        'service_name': os.environ['TEST_SERVICE_NAME'],
        'service_secret': os.environ['TEST_SERVICE_SECRET'],
        'grant_type': 'client_credentials',
        }

@pytest.fixture()
def good_client_id():
    return os.environ['TEST_CLIENT_ID']

@pytest.fixture()
def bad_client_id():
    return 1

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

@pytest.fixture(scope='module')
def client():
    app = create_app(config={"TESTING": True})
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
