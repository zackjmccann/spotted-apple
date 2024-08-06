"""Class handling Spotify Web API requests"""
import os
import time
import base64
import urllib
import requests
import webbrowser
from auth.oauth import OAuthBase, AuthenticationError

DEV_MODE = os.getenv('DEV_MODE')

class SpotifyOAuth(OAuthBase):
    """
    Authorization for Spotify's OAuth flow

    For the purpose of this application/implemenation, the class
    assumes the appropriate environment variables are present.

    Parameters
            - requests_session: A Requests Session
            - requests_timeout: Optional, tell Requests to stop waiting for a response after
                                a given number of seconds
            - state           : Can be passed to associate a specific user to a Spotify instance, particularly for
                                authorization. The user_id is sent to the Spotify Web API, and returned with an authorization code.
                                The code can then be associated with the user_id, and leveraged to update the authorization
                                across streamlit sessions.
    """
    def __init__(self, requests_session=None, requests_timeout=None, state=None):
        super().__init__(requests_session)
        self.authorization_url = 'https://accounts.spotify.com/authorize'
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = self._get_redirect_url(self)
        self.state = state = os.getenv('SPOTIFY_STATE') if not DEV_MODE else os.getenv('SPOTIFY_DEV_STATE')
        self.authorization_headers = self._make_authorization_headers()
        self.scope = 'user-read-private user-read-email'  # TODO: Hardcoded for simplicity, change if needed
        self.requests_timeout = requests_timeout # TODO: check "requests_timeout" implementation

    def authorize(self):
        response_type = 'code'
        payload = urllib.parse.urlencode({
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': self.state,
            'scope': 'user-read-private user-read-email'
            })
        webbrowser.open(self.authorization_url + '?' + payload, new=0)
        return self.authorization_url + '?'  + payload

    def get_access_token_info(self, code: str):
        payload = {
            'redirect_uri': self.redirect_uri,
            'code': code,
            'grant_type': "authorization_code",
            'scope': self.scope,
            'state': self.state,
            }
    
        headers = self._make_authorization_headers()

        try:
            response = self.requests_session.post(
                self.token_url,
                data=payload,
                headers=headers,
                verify=True,
                timeout=self.requests_timeout,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_error:
            self._handle_oauth_error(http_error)

    def refresh_access_token(self, refresh_token):
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        headers = self._make_authorization_headers()

        try:
            response = self._session.post(
                self.token_url,
                data=payload,
                headers=headers,
                timeout=self.requests_timeout,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_error:
            self._handle_oauth_error(http_error)

    def _make_authorization_headers(self):
        auth_header = base64.b64encode(
            str(self.client_id + ":" + self.client_secret).encode("ascii")
        )
        return {"Authorization": f"Basic {auth_header.decode('ascii')}"}

    @staticmethod
    def _get_redirect_url(self):
        """The redirect URL should lead back to the appropriate Streamlit App page"""
        # TODO: Not inherently part of 'Spotify', think about how to abstract better
        HOST = os.getenv('HOST')
        PORT = os.getenv('PORT')

        if not PORT or not HOST:
            raise NameError('Host and/or Port are not defined in the environment, cannot redirect.')
        
        if not DEV_MODE:
            return f'http://{HOST}/' # TODO: Add https when SSL cert is provisioned
        else:
            return f'http://{HOST}:{PORT}/auth_landing'