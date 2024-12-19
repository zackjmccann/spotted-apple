import os
import requests


SECRET_KEY = os.getenv('SECRET_KEY')
ALOGRITHMS = os.getenv('JWT_ALORITHM')
APP_ID = os.getenv('APP_ID')
GRANTED_APP_IDS = os.getenv('GRANTED_APP_IDS')

class AuthenticationError(Exception):
    pass

if None in [SECRET_KEY, ALOGRITHMS, APP_ID]:
    raise AuthenticationError('An authentication failure occurred')

def authenticate_with_auth_server(request):
    access_token = None
    access_token = request.headers['Authorization'].split(" ")[1]

    if is_valid_token(access_token):
        return {'code': 200, 'valid': True}
    else:
        return {'code': 401, 'valid': False}

def is_valid_token(access_token):
    response = call_auth_server('/auth/introspect', {'access_token': access_token})
    if response.status_code == 401:
        return False
    else:
        return True

def call_auth_server(endpoint, payload, headers = None):
    AUTH_SERVICE = os.getenv('AUTH_SERVICE')
    response = requests.post(f'http://{AUTH_SERVICE}{endpoint}', json=payload, headers=headers)
    return response
