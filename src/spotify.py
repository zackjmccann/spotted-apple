"""
Class handling Spotify Web API requests
"""

import os
import base64
import requests
import webbrowser
import urllib
import time
from auth import OAuthBase, AuthenticationError
from helpers import (
    RequestHandler,
    LocalHTTPServer,
    create_local_http_server,
    get_host_port,
    handle_app_request,
    check_if_user_has_app_access,
    validate_email_input
    )
from http.server import BaseHTTPRequestHandler, HTTPServer

DEV_MODE = os.getenv('DEV_MODE')


class SpotifyOAuth(OAuthBase):
    """
    Authorization for Spotify's OAuth flow

    For the purpose of this application/implemenation, the class
    assumes the appropriate environment variables are present.
    """
    def __init__(self, requests_session=None, requests_timeout=None):
        # TODO: check "requests_timeout" implementation
        """
        Creates a SpotifyOAuth object

        Parameters
             - requests_session: A Requests Session
             - requests_timeout: Optional, tell Requests to stop waiting for a response after
                                 a given number of seconds
        """
        super().__init__(requests_session)
        self.authorization_url = 'https://accounts.spotify.com/authorize'
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = self._get_redirect_url(self)
        self.state = os.getenv('SPOTIFY_STATE') if not DEV_MODE else os.getenv('SPOTIFY_DEV_STATE')
        self.authorization_headers = self._make_authorization_headers()
        self.scope = 'user-read-private user-read-email'  # TODO: Hardcoded for simplicity, change if needed
        self.cache_handler = None  # TODO: Caching with Redis?
        self.requests_timeout = requests_timeout


    def authorize(self, auto_open=True):
        response_type = 'code'
        payload = urllib.parse.urlencode({
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'user-read-private user-read-email'
            })
        if auto_open:
            webbrowser.open_new_tab(self.authorization_url + '?' + payload)
        else:
            return self.authorization_url + '?'  + payload

    def validate_token(self, token_info):
        # End the request if there is no token
        if token_info is None:
            return None

        if self.is_token_expired(token_info):
            return self.refresh_access_token(token_info["refresh_token"])

    def get_authorize_url(self, state=None):
        response_type = "code"

        payload = urllib.parse.urlencode(
            {
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "response_type": "code",
                "scope": self.scope,
                "state": self.state,
            }
        )

        return f"{self.authorization_url}?{payload}"

    def get_authorization_code(self, response=None):
        if response:
            return self.parse_response_code(response) # TODO: parse_response_code expects a URL
        return self._get_auth_response()

    def parse_response_code(self, url):
        _, code = self.parse_auth_response_url(url)
        if code is None:
            return url
        else:
            return code

    def _get_auth_response(self):
        # TODO: Revisit how your planning on using this class
        #       within a Streamlit App and your Spotted Apple App. If 
        #       Spotted Apple's redirect URL is a running Streamlit App, there's
        #       likely no need to start a local/seperate server to field the redirect
        #       from Spotify's auth flow. Just read the URL on a given streamlit page load
        #       a parse it for a "code" parameter (then try to exchange it for a token).
        #       Depending on how that's implemented will determine how it's coupled to this class
        #       and whether a local/seperate server is needed.
        redirect_info = urlparse(self.redirect_uri)
        redirect_host, redirect_port = get_host_port(redirect_info.netloc)
        redirected_url = self._get_redirect_url()
        server = start_local_http_server(redirect_port)
        server.handle_request()
        state, code = SpotifyOAuth.parse_auth_response_url(redirected_url)

        if server.error is not None:
            raise server.error
        elif self.state != state:
            raise AuthenticationError(
                message="Unexpected state recieved by the server.",
                error=404, #TODO: Check if this is right
                error_description='State Error')
        elif server.auth_code is not None:
            return server.auth_code
        else:
            raise AuthenticationError( "Server listening on localhost has not been accessed")


        return code

    def get_access_token(self, code=None, check_cache=True):
        """
        Get the access token provided by authentication response code
        """

        if check_cache:
            token_info = self.validate_token(self.cache_handler.get_cached_token())
            if token_info is not None:
                if self.is_token_expired(token_info):
                    token_info = self.refresh_access_token(token_info["refresh_token"])
                return token_info if as_dict else token_info["access_token"]

        payload = {
            'redirect_uri': self.redirect_uri,
            'code': code or self.get_auth_response(),
            'grant_type': "authorization_code",
            'scope': self.scope,
            'state': self.state,
            }
    
        headers = self._make_authorization_headers()

        try:
            response = self._session.post(
                self.token_url,
                data=payload,
                headers=headers,
                verify=True,
                timeout=self.requests_timeout,
            )
            response.raise_for_status()
            token_info = response.json()
            token_info = self._add_token_metadata(token_info)
            self.save_token_to_cache(token_info)
            return token_info["access_token"]
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
            token_info = response.json()
            token_info = self._add_token_metadata(token_info)
            if "refresh_token" not in token_info:
                token_info["refresh_token"] = refresh_token
            self.save_token_to_cache(token_info)
            return token_info
        except requests.exceptions.HTTPError as http_error:
            self._handle_oauth_error(http_error)

    def _add_token_metadata(self, token_info):
        """Add metadata for application"""
        token_info.update({
            "expiration_timestamp": int(time.time()) + token_info["expires_in"]
            })
        return token_info

    def save_token_to_cache(self, token_info):
        # TODO: Add Redis cache here
        pass

    def _make_authorization_headers(self):
        auth_header = base64.b64encode(
            str(self.client_id + ":" + self.client_secret).encode("ascii")
        )
        return {"Authorization": f"Basic {auth_header.decode('ascii')}"}

    @staticmethod
    def parse_auth_response_url(url):
        query_string = urllib.parse.urlparse(url).query
        response_parameters = dict(urllib.parse.parse_qsl(query_string))

        if "error" in response_parameters:
            raise AuthenticationError(
                message=f"Auth server error: {response_parameters['error']}",
                error=response_parameters["error"]
            )
        else:
            return response_parameters

    @staticmethod
    def _get_redirect_url(self):
        """The redirect URL should lead back to the appropriate Streamlit App page"""
        # TODO: Not inherently part of 'Spotify', think about how to abstract better
        DEV_MODE = os.getenv('DEV_MODE')
        HOST = os.getenv('HOST')
        PORT = os.getenv('PORT')

        if not PORT or not HOST:
            raise NameError('Host and/or Port are not defined in the environment, cannot redirect.')
        
        if not DEV_MODE:
            return f'http://{HOST}/' # TODO: Add https when SSL cert is provisioned
        else:
            return f'http://{HOST}:{PORT}/'
