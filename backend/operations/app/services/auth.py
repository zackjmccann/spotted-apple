import os
import json
import requests
from jsonschema import validate, ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from urllib.parse import urlencode
from models.login import login_payload_schema
from models.client_credentials import client_credentials_payload_schema
from models.session import session_payload_schema
from utilities.payload_handlers import sanitize
from database import aloe


SECRET_KEY = os.getenv('SECRET_KEY')
ALOGRITHMS = os.getenv('JWT_ALORITHM')
APP_ID = os.getenv('APP_ID')
GRANTED_APP_IDS = os.getenv('GRANTED_APP_IDS')

class AuthenticationError(Exception):
    pass

if None in [SECRET_KEY, ALOGRITHMS, APP_ID]:
    raise AuthenticationError('An authentication failure occurred')

def validate_authorization_token(request):
    access_token = None
    access_token = request.headers['Authorization'].split(" ")[1]

    if is_valid_token(access_token):
        return {'code': 200, 'valid': True}
    else:
        return {'code': 401, 'valid': False}

def authenticate_with_auth_server(request):
    try:
        AUTH_SERVICE = os.getenv('AUTH_SERVICE')
        CLIENT_ID = os.getenv('CLIENT_ID')

        payload = request.get_json()
        validate(instance=payload, schema=login_payload_schema)

        query_parameters = {
            'client_id': CLIENT_ID, # TODO: Clients should provide this, not the ops server?
            'redirect_uri': 'http://localhost:8000/auth/callback', # TODO: Don't hard code this
            'state': 'state',
            'response_type': 'code',
            'scope': 'profile offline_access openid',
            'code_challenge': 'code_challenge',
            'code_challenge_method': 'S256',
            'email': payload.get('email'),
            'password': payload.get('password'),
            'grant_type': payload.get('grant_type'),
        }

        params = urlencode(query_parameters)
        auth_service = f'http://{AUTH_SERVICE}/auth/authorize'

        jar = requests.cookies.RequestsCookieJar()
        jar.set('oauth_state', 'state', secure=False, rest={"HttpOnly": True},)
        jar.set('oauth_code', 'code_challenge', secure=False, rest={"HttpOnly": True},)

        return requests.get(
            url=auth_service,
            params=params,
            headers=request.headers,
            cookies=jar)

    except (UnsupportedMediaType, ValidationError):
        raise AuthenticationError('Failed to login')

def is_valid_token(access_token):
    # TODO: Can be refactored to raise an AuthenticationError
    response = call_auth_server('/auth/introspect', {'access_token': access_token})
    if response.status_code == 401:
        return False
    else:
        return True

def call_auth_server(endpoint, payload, headers = None):
    AUTH_SERVICE = os.getenv('AUTH_SERVICE')
    response = requests.post(f'http://{AUTH_SERVICE}{endpoint}', json=payload, headers=headers)
    return response

def exchange_code_for_tokens(code: str, state: str):
    return {
        'id': code,
        'access': code,
        'refresh': code
    }

def client_is_authenticated(payload: dict): # TODO: Change to something like authenticate_client (use a verb)
    playload_mapping = {
        'id': 'str',
        'username': 'str',
        'password': 'str',
        'grant_type': 'str',
        }

    clean_payload = sanitize(payload, client_credentials_payload_schema, playload_mapping)

    try:
        # TODO: Consider if there should be more checks for this service
        AUTH_SERVICE = os.getenv('AUTH_SERVICE')
        url = f'http://{AUTH_SERVICE}/auth/authorize/client'
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(clean_payload)

        response = requests.post(url=url, data=body, headers=headers)

        if response.status_code != 200:
            return False

        return True

    except AuthenticationError:
        return False

def create_session(payload: dict):
    if client_is_authenticated(payload):
        print('Creating session...')
        response = aloe.create_session()
        if response != {}:
            try:
                return {
                    'id': response['session_id'],
                    'state': response['session_state'],
                    'created': response['created_at'],
                    'expires': response['expires_at'],
                    }
            except KeyError:
                raise AuthenticationError
    raise AuthenticationError

def validate_session(payload: dict):
    playload_mapping = {'session_id': 'str'}
    clean_payload = sanitize(payload, session_payload_schema, playload_mapping)
    try:
        response = aloe.validate_session(clean_payload['session_id'])
        if not response:
            return False
        return response['valid']
    except AuthenticationError:
        return False

def authenticate_user_account(payload: dict):
    try:
        session_payload = {'session_id': payload.get('session_id', None)}
        if validate_session(session_payload):
            # The sanitizing logic below is redundate to validate_session logic, but 
            # generally do not want to pass direct user inputs to DB.
            session_playload_mapping = {'session_id': 'str'}
            clean_session_payload = sanitize(session_payload, session_payload_schema, session_playload_mapping)
            session_state_response = aloe.get_session_state(clean_session_payload['session_id'])
            payload.update(session_state_response)
            playload_mapping = {
                'client_id': 'str',
                'state': 'str',
                'response_type': 'str',
                'scope': 'str',
                # 'code_challenge': 'str',
                # 'code_challenge_method': 'str',
                'email': 'str',
                'password': 'str',
                'grant_type': 'str',
            }
            clean_payload = sanitize(payload, login_payload_schema, playload_mapping)

            AUTH_SERVICE = os.getenv('AUTH_SERVICE')
            url = f'http://{AUTH_SERVICE}/auth/authorize/user'
            headers = {'Content-Type': 'application/json'}
            body = json.dumps(clean_payload)
            response = requests.post(url=url, data=body, headers=headers)
            if response.status_code != 200:
                raise AuthenticationError
            data = response.json()
            return data
        raise AuthenticationError
    except (KeyError, AuthenticationError):
        raise AuthenticationError
