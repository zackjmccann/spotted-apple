import os
import re
import pytest
import requests
from src.auth.oauth import AuthenticationError


def test_make_authorization_headers(spotify_oauth):
    authorization_headers = spotify_oauth._make_authorization_headers()
    regex = r'Basic*'
    key = re.search(regex, authorization_headers['Authorization'])
    assert 'Authorization' in authorization_headers
    assert key is not None

def test_get_access_token_info(spotify_oauth):
    auth_code = os.getenv('AUTHORIZATION_CODE')
    access_token_info = spotify_oauth.get_access_token_info(auth_code)
    # access_token
    # token_type
    # scope
    # expires_in
    # refresh_token
    assert access_token_info == 1


def test_refresh_access_token(spotify_oauth):
    pass