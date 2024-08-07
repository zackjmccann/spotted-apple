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
