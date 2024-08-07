import os
import time
import requests
import pytest
from src.auth.spotify import SpotifyOAuth
from src.db.postgres import Postgres
from src.db.spotted_apple_db import SpottedAppleDB


@pytest.fixture
def new_request_session():
    return requests.Session()

@pytest.fixture
def valid_token():
    expiration_timestamp = int(time.time())
    return {
        "expires_in": 3600,
        "expiration_timestamp": expiration_timestamp,
        "scope": 'user-read-private user-read-email'
        }

@pytest.fixture
def expired_token():
    expiration_timestamp = int(time.time())
    return {
        "expiration_timestamp": expiration_timestamp + 80
        }

@pytest.fixture
def spotify_oauth():
    return SpotifyOAuth()

@pytest.fixture
def postgres():
    return Postgres()

@pytest.fixture
def spotted_apple_db():
    return SpottedAppleDB()
