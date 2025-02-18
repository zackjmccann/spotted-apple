import os
import jwt
import json
import datetime
from distutils.util import strtobool
from models.client_credentials import client_credentials_payload_schema
from models.login import login_payload_schema
from models.auth_code_exchange import auth_code_payload_schema
from utilities.payload_handlers import sanitize
from jsonschema import ValidationError
from database import aloe

SECRET_KEY = os.getenv('SECRET_KEY')
ALOGRITHMS = os.getenv('JWT_ALORITHM')
APP_ID = os.getenv('APP_ID')
GRANTED_APP_IDS = os.getenv('GRANTED_APP_IDS')

class AuthenticationError(Exception):
    pass

if None in [SECRET_KEY, ALOGRITHMS, APP_ID]:
    raise AuthenticationError('An authentication failure occurred')

def authenticate_client(payload):
    try:
        playload_mapping = {'client_id': 'str', 'username': 'str', 'secret': 'str', 'grant_type': 'str'}
        clean_payload = sanitize(payload, client_credentials_payload_schema, playload_mapping)
        response = aloe.authenticate_client(clean_payload)
        clean_payload.update(response)

        if not response['valid']:
            raise AuthenticationError

        return clean_payload
    except (ValidationError, ValueError, KeyError):
        raise AuthenticationError

def get_authorization_code(payload):
    try:
        playload_mapping = {
            'client_id': 'str',
            'client_secret': 'str',
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
        response = aloe.authenticate_user({
            'email': clean_payload.get('email', ''),
            'password': clean_payload.get('password', ''),
        })
        
        if response['valid']:
            authorization_code = generate_authorization_code()
        return authorization_code

    except (KeyError, ValidationError):
        raise AuthenticationError

def generate_authorization_code():
    response = aloe.issue_authorization_code()
    return response['auth_code']

def exchange_auth_code_for_tokens(payload: dict):
    try:
        playload_mapping = {
                'client_id': 'str',
                'state': 'str',
                'client_secret': 'str',
                'code': 'str',
                'grant_type': 'str',
                'response_type': 'str',
                'scope': 'str',
            }
        clean_payload = sanitize(payload, auth_code_payload_schema, playload_mapping)
        response = aloe.validate_authorization_code(clean_payload.get('code', ''))
        clean_payload.update(response)

        if not response['valid']:
            raise AuthenticationError

        return clean_payload
    except (ValidationError, ValueError, KeyError):
        raise AuthenticationError

def issue_token(username, id, exp=5):
    data = {
        'iss': 'spotted-apple-backend',
        # 'sub' user_id TODO: Try to implement this
        'aud': [str(id)], # TODO: change to client_id
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=exp),
        'jti': 'backend_services' + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M'),
        'context': {
            'username': username,
            'roles':['client']
            }
        }
    return jwt.encode(data, SECRET_KEY, ALOGRITHMS)

def validate_token(token):
    if not token:
        return {
            'valid': False,
            'code': 400,
            'status': 'Authentication Failed',
            'message': 'Missing Token',
        }

    try:
        assert not is_blacklisted_token(token)
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALOGRITHMS], audience=APP_ID)
        # TODO: Test GRANTED_APP_IDS = json.loads(os.environ['GRANTED_APP_IDS'])
        # for aud in data['aud']:
        #     assert aud in GRANTED_APP_IDS

        return {'valid': True, 'code': 200, 'data': data,}

    except AssertionError:
        error_data = {
            'status': 'Authentication Failed',
            'message': 'Token Blacklisted'
            }

    except jwt.ExpiredSignatureError:
        error_data = {
            'status': 'Authentication Failed',
            'message': 'Token Expired'
            }

    except jwt.InvalidTokenError:
        error_data = {
            'status': 'Authentication Failed',
            'message': 'Invalid Token'
            }

    response = {'valid': False, 'code': 401}
    response.update(error_data)
    return response

def set_cookies(response, tokens: list):
    httponly=True
    samesite='Strict'
    secure=True

    dev_mode = bool(strtobool(os.getenv('DEV_MODE', 'false')))
    if dev_mode:
        secure = False  # Use True when app is using HTTPS

    cookie_configs = {
        'access_token': {'max_age': 60 * 15}, # 15 minutes
        'refresh_token': {'max_age': 7 * 24 * 60 * 60}, # 7 days
    }

    for token in tokens:    
        response.set_cookie(
            token['type'],
            token['token'],
            httponly=httponly,
            samesite=samesite,
            secure=secure,
            max_age=cookie_configs[token['type']].get('max_age')
        )

    return response

def is_blacklisted_token(token):
    response = aloe.check_token_blacklist(token)
    return response['token_is_blacklisted']

def blacklist_token(token):
    response = aloe.blacklist_token(token)

    if response['id'] is None:
        response.update({
            'code': 401,
            'status': 'Authentication Failed',
            'message': 'Unable to authenticate',
        })
    
    return {
        'code': 200,
        'status': 'Success',
        'message': 'Token blacklisted',
        }

def parse_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALOGRITHMS], audience=APP_ID)
