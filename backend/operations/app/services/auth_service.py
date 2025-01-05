import json
import requests
from requests import Response
from urllib3.exceptions import HTTPError
from models import (
    login_payload_schema,
    client_credentials_payload_schema, 
    auth_code_payload_schema,
    session_payload_schema,
)
from jsonschema import ValidationError
from utilities.payload_handlers import sanitize
from app.services import BaseService


class AuthenticationError(Exception):
    pass


class AuthService(BaseService):
    def __init__(self):
        super().__init__()
        self.server = self._get_environment_variable('AUTH_SERVER')
        self.secret = self._get_environment_variable('AUTH_SECRET')
        self.client_id = self._get_environment_variable('AUTH_CLIENT_ID')

    def authenticate_client(self, payload: dict) -> bool:
        """
        Authenticate a client with the Authentication Service.

        Clients payloads are validated and sent to the auth service. Payload
        should contain the following:
            id: The client id, which should be registered with the auth service
            username: Client username
            secret: secret associated with the client on the auth service
        """
        response = self._request_auth_service(
            method='POST',
            endpoint='/auth/authorize/client',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(payload),
        )

        if response.status_code != 200:
            raise AuthenticationError('Unable to authenticate client')
        return True

    def authenticate_user_account(self, payload: dict) -> dict:
        try:
            payload.update({
                'response_type': 'code',
                'scope': 'profile offline_access openid'
                })
            
            response = self._request_auth_service(
                method='POST',
                endpoint='/auth/authorize/user',
                headers={'Content-Type': 'application/json'},
                body=json.dumps(payload),
            )
            if response.status_code != 200:
                raise AuthenticationError('Unable to authenticate user')
            
            data = response.json()
            echoed_state = data.get('state', None)
            assert payload.get('state') == echoed_state
            return data
        except (AssertionError, AttributeError):
            raise AuthenticationError('Unable to authenticate user.')

    def exchange_authentication_code(self, payload: dict) -> dict:
        try:
            payload.update({
                'response_type': 'tokens',
                'scope': 'profile offline_access openid'
                })
            response = self._request_auth_service(
                method='POST',
                endpoint='/auth/token',
                headers={'Content-Type': 'application/json'},
                body=json.dumps(payload),
            )
            if response.status_code != 200:
                raise AuthenticationError('Unable to retrieve access tokens')
            
            data = response.json()
            echoed_state = data.get('state', None)
            assert payload.get('state') == echoed_state
            return data
        except (AssertionError, AttributeError):
            raise AuthenticationError('Unable to authenticate user.')

    def _request_auth_service(self, method: str, endpoint: str, headers: dict, body: dict) -> Response:
        """Initiate an HTTP/S request to the authentication service"""
        url = f'{self.server}/{endpoint}'
        try:
            return getattr(requests, method.lower())(
                url=url,
                data=body,
                headers=headers)
        except (HTTPError, requests.exceptions.ConnectionError) as err:
            raise AuthenticationError(f'An unexpected error occurred: {err}')   

    @staticmethod
    def sanitize_payload(raw_payload: dict, payload_type: str) -> dict:
        if payload_type == 'client':
            playload_mapping = {
                'client_id': 'str',
                'username': 'str',
                'secret': 'str',
                'grant_type': 'str',
                }
            schema = client_credentials_payload_schema

        elif payload_type == 'session':
            playload_mapping = {
                'session': 'str',
                'client_id': 'str'
            }
            schema = session_payload_schema

        elif payload_type == 'login':
            playload_mapping = {
                'client_id': 'str',
                'client_secret': 'str',
                'state': 'str',
                'email': 'str',
                'password': 'str',
                'grant_type': 'str',
                }
            schema = login_payload_schema

        elif payload_type == 'auth_code':
            playload_mapping = {
                'client_id': 'str',
                'client_secret': 'str',
                'state': 'str',
                'code': 'str',
                'grant_type': 'str',
                }
            schema = auth_code_payload_schema

        else:
            raise AuthenticationError('Unsupported payload.')

        try:      
            return sanitize(raw_payload, schema, playload_mapping)
        except ValidationError:
            raise AuthenticationError('Unable to authenticate user.')
