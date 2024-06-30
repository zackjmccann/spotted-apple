"""
Class handling Spotify Web API requests
"""
import os
import requests
import webbrowser
import urllib


class Spotify:
    def __init__(self):
        self.base_url = 'https://accounts.spotify.com/authorize?'
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = self._get_redirect_url(self)
        self.state = os.getenv('SPOTIFY_STATE')

    def authorize(self, auto_open=True):
        response_type = 'code'
        payload = urllib.parse.urlencode({
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'user-read-private user-read-email'
            })
        if auto_open:
            webbrowser.open_new_tab(self.base_url + payload)
        else:
            return self.base_url + payload

    @staticmethod
    def _get_redirect_url(self):
        """The redirect URL should lead back to the appropriate Streamlit App page"""
        # TODO: Not inherently part of Spotify, think about how to abstract better
        STREAMLIT_PORT = os.getenv('STREAMLIT_PORT')
        STREAMLIT_HOST = os.getenv('STREAMLIT_HOST')

        if not STREAMLIT_PORT or not STREAMLIT_HOST:
            raise NameError('Streamlit Host and/or Port are not defined in the environment, cannot redirect.')
        
        return f'http://{STREAMLIT_HOST}:{STREAMLIT_PORT}/'
