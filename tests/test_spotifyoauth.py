import os
import re
import pytest
import requests
from src.auth import AuthenticationError

"""
# TODO: Build tests for methods below:
    - refresh_access_token()
    - validate_token()
    - get_access_token()
    - save_token_to_cache()
"""

def test_make_authorization_headers(spotify_oauth):
    authorization_headers = spotify_oauth._make_authorization_headers()
    regex = r'Basic*'
    key = re.search(regex, authorization_headers['Authorization'])
    assert 'Authorization' in authorization_headers
    assert key is not None

def test_add_token_metadata(spotify_oauth, valid_token):
    token_info = spotify_oauth._add_token_metadata(valid_token)
    assert 'expiration_timestamp' in token_info

def test_get_authorize_url(spotify_oauth):
    auth_url = spotify_oauth.get_authorize_url()
    response = requests.get(auth_url)
    assert response.status_code == 200

def test_parse_access_granted_auth_response_url(spotify_oauth, access_granted_redirect_uri):
    expected_parameters = {
        'code': os.getenv('SPOTIFY_DEV_CODE'),
        'state': os.getenv('SPOTIFY_DEV_STATE')
        }
    params = spotify_oauth.parse_auth_response_url(access_granted_redirect_uri)
    assert params == expected_parameters

def test_parse_access_denied_auth_response_url(spotify_oauth, access_denied_redirect_uri):
    with pytest.raises(Exception) as err:
        spotify_oauth.parse_auth_response_url(access_denied_redirect_uri)
    assert 'AuthenticationError' in str(err)

def test_parse_response_code(spotify_oauth, access_granted_redirect_uri):
    response_code = spotify_oauth.parse_auth_response_url(access_granted_redirect_uri)
    code = 'NApCCg..BkWtQ'
    assert response_code == code
