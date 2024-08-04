import time
import requests


class AuthenticationError(Exception):
    """
    General purpose Error to raise during Auth Code for Spotify
    and/or Apple Music.
    """
    def __init__(self, message, error=None, error_description=None, *args, **kwargs):
        self.error = error
        self.error_description = error_description
        self.__dict__.update(kwargs)
        super().__init__(message, *args, **kwargs)


class OAuthBase:
    def __init__(self, requests_session):
        self.requests_session = self._get_requests_session(self, requests_session)

    @staticmethod
    def _get_requests_session(self, requests_session):
        """Check or build the request session"""
        if isinstance(requests_session, requests.Session):
            return requests_session
        else:  # Build a new session.
            return requests.Session()

    @staticmethod  # TODO: Review this method
    def is_token_expired(token_info):
        now = int(time.time())
        return token_info["expiration_timestamp"] - now < 60

    def _handle_oauth_error(self, http_error):
        """
        First, check if the response can be decoded into JSON, and if not, raise a ValueError.
        Next, try to decode it into text. If an empty string is received (which is falsy), set
        the error description to "Uknown".
        """
        response = http_error.response
        try:
            error_payload = response.json()
            error = error_payload.get("error")
            error_description = error_payload.get("error_description")
        except ValueError:
            error = response.text or None
            error_description = "Unknown"

        raise AuthenticationError(
            message=f"error: {error}, error_description: {error_description}",
            error=error,
            error_description=error_description,
        )

    def close_connection_pool(self):
        """Close connection pool"""
        # TODO: Consider if this should check anything or try/except
        self.requests_session.close()
