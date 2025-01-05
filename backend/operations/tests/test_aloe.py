import os
import pytest
from app.database import aloe
from app.models import session_schema
from jsonschema import ValidationError
from app.utilities.payload_handlers import validate_with_datetime


@pytest.fixture
def aloe_db():
    return aloe

@pytest.fixture
def bad_client_id():
    return 1

@pytest.fixture
def good_client_id():
    return os.environ['TEST_CLIENT_ID']

@pytest.fixture()
def session(aloe_db, good_client_id):
    session = aloe_db.create_session(good_client_id)
    yield session
    revoked = aloe_db.revoke_session(session['session_id'])
    assert revoked
    pass

def test_aloe_create_session(session):
    validate_with_datetime(session, session_schema)
