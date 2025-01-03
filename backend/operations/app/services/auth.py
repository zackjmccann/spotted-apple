import os
import jwt
import json
import requests
import datetime
from models.login import login_payload_schema
from models.client_credentials import client_credentials_payload_schema, client_id_payload_schema
from models.auth_code_exchange import auth_code_exchange_payload_schema
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
        client_id_playload_mapping = {'id': 'str'}
        clean_client_id_payload = sanitize(payload, client_id_payload_schema, client_id_playload_mapping)
        response = aloe.create_session(clean_client_id_payload.get('id', ''))
        if response != {}:
            try:
                sesssion_token = issue_session_token(response)
                return {
                    'token': sesssion_token,
                    'expires': response['expires_at']
                    }
            except KeyError:
                raise AuthenticationError
    raise AuthenticationError

def validate_session(payload: dict):
    playload_mapping = {'session': 'str', 'client_id': 'str'}
    clean_payload = sanitize(payload, session_payload_schema, playload_mapping)
    try:
        session_id = validate_token(clean_payload)
        response = aloe.validate_session(session_id)
        if not response:
            return False
        return response['valid']
    except AuthenticationError:
        return False

def authenticate_user_account(payload: dict):
    try:
        session_payload_mapping = {'session': 'str', 'client_id': 'str'}
        session_payload = {'session': payload.get('session', None), 'client_id': payload.get('client_id')}
        clean_session_payload = sanitize(session_payload, session_payload_schema, session_payload_mapping)
        if validate_session(clean_session_payload):
            session_id = validate_token(clean_session_payload)
            session_state_response = aloe.get_session_state(session_id)
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

def exchange_authentication_code(payload: dict):
    try:
        playload_mapping = {'session': 'str', 'client_id': 'str'}
        clean_payload = sanitize(payload, session_payload_schema, playload_mapping)
        if validate_session(clean_payload):
            session_id = validate_token(clean_payload)
            session_state_response = aloe.get_session_state(session_id)
            payload.update(session_state_response)
            playload_mapping = {
                'client_id': 'str',
                'state': 'str',
                # 'client_secret': 'str',
                'code': 'str',
                'grant_type': 'str',
            }
            clean_payload = sanitize(payload, auth_code_exchange_payload_schema, playload_mapping)

            AUTH_SERVICE = os.getenv('AUTH_SERVICE')
            url = f'http://{AUTH_SERVICE}/auth/token'
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

def validate_authorization_token(request):
    access_token = None
    access_token = request.headers['Authorization'].split(" ")[1]

    if is_valid_token(access_token):
        return {'code': 200, 'valid': True}
    else:
        return {'code': 401, 'valid': False}

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

def issue_session_token(session_data: dict):
    data = {
        'iss': 'spotted-apple-ops-backend',
        'aud': [session_data['client_id']],
        'iat': session_data['created_at'],
        'exp': session_data['expires_at'],
        # 'iat': datetime.datetime.strptime(session_data['created_at'], '%Y-%m-%d %H:%M:%S.%f %z'),
        # 'exp': datetime.datetime.strptime(session_data['expires_at'], '%Y-%m-%d %H:%M:%S.%f %z'),
        'jti': 'backend_services' + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M'),
        'context': {
            'id': session_data['session_id'],
            # 'state': session_data['session_state'],
            'roles':['client']
            }
        }
    return jwt.encode(data, SECRET_KEY, ALOGRITHMS)


def validate_token(payload):
    token = payload.get('session', '')
    client_id = payload.get('client_id', '')

    if not token:
        raise AuthenticationError

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALOGRITHMS], audience=client_id)
        return data['context']['id']

    except jwt.ExpiredSignatureError:
        print('Token Expired') # TODO: Add logger
        raise AuthenticationError

    except jwt.InvalidTokenError:
        print('Token Invalid') # TODO: Add logger
        raise AuthenticationError
