"""
Class handling Spotify Web API requests
"""
import os
import requests

class Spotify:
    def __init__(self):
        self.base_url = 'https://accounts.spotify.com/authorize?'
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        self.state = os.getenv('SPOTIFY_STATE')

    def authorize(self):
        response_type = 'code'
        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'user-read-private user-read-email'
            }

        r = requests.get(self.base_url, params=payload)
