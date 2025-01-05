import pytest
import datetime
from app.services import SessionError

def test_session_service_validate_session(session, good_client_id):
    assert session['client_id'] == good_client_id
    assert session['expires_at'] > datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)

def test_session_service_fail_to_create_session(session_service, bad_client_id):
    with pytest.raises(SessionError):
        session = session_service.create_session(bad_client_id)

def test_session_service_revoke_session(session_service, good_client_id):
    session = session_service.create_session(good_client_id)
    revoked = session_service.revoke_session(session['session_id'])
    assert revoked

def test_session_service_validate_bad_session(session_service, invalid_session):
    is_valid = session_service.validate_session(invalid_session['session_id'])
    assert not is_valid
