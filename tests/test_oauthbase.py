import io
import time
import pytest
import requests
from src.auth import OAuthBase
from src.auth import AuthenticationError
from urllib.error import HTTPError
from requests.models import Response

@pytest.fixture
def new_request_session():
    return requests.Session()

@pytest.fixture
def oauth_base(new_request_session):
    return OAuthBase(new_request_session)

@pytest.fixture
def fake_valid_token():
    expires_at = int(time.time())
    return {
        "expires_at": expires_at
        }

@pytest.fixture
def fake_expired_token():
    expires_at = int(time.time())
    return {
        "expires_at": expires_at + 80
        }

@pytest.fixture
def http_error():
    # Create response
    response = Response()
    response.code = 'Not Found'
    response.error_type = 'Not Found'
    response.status_code = 404
    response._content = b'{ "error": "URL Not Found", "error_description":  "bad url"}'

    # Create HTTPError and add response
    url = 'bad url'
    code = 404
    msg = 'Not Found: bad url'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    f = io.BytesIO(b"\x00\x01")
    http_error = HTTPError(url, code, msg, headers, f)
    http_error.response = response

    return http_error

def test_get_requests_session(oauth_base):
    assert isinstance(oauth_base.requests_session, requests.Session)

def test_create_requests_session():
    oauth_base = OAuthBase(None)
    assert isinstance(oauth_base.requests_session, requests.Session)

def test_expired_token(oauth_base, fake_expired_token):
    assert not oauth_base.is_token_expired(fake_expired_token)

def test_valid_token(oauth_base, fake_valid_token):
    assert oauth_base.is_token_expired(fake_valid_token)

def test_handle_oauth_error(oauth_base, http_error):
    with pytest.raises(AuthenticationError):
        oauth_base._handle_oauth_error(http_error)
