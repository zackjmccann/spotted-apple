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
    # TODO: Refactor route to call to the auth endpoint
    access_token = None
    access_token = request.headers['Authorization'].split(" ")[1]

    if is_valid_token(access_token):
        return {'valid': True, 'code': 200}
    
    data = request.get_json()
    response = refresh_tokens(data.get('refresh_token', None))
    
    if response['tokens_refreshed']:
        return {'valid': True, 'code': 200}

    return {
        'code': 400,
        'valid': False,
        'status': response['status'],
        'message': response['message']
    }

def is_valid_token(access_token):
    response = call_auth_server('introspect', {'access_token': access_token})
    data = response.json()
    return data['valid']

def refresh_tokens(refresh_token):
    response = call_auth_server('refresh', {'refresh_token': refresh_token})
    if response['status_code'] == 200:
        return {'tokens_refreshed': True}
    
    data = response.get_json()
    data.update({'tokens_refreshed': False})
    return data

def call_auth_server(endpoint, payload):
    AUTH_SERVICE = os.getenv('AUTH_SERVICE')
    response = requests.post(f'http://{AUTH_SERVICE}/auth/{endpoint}', json=payload)
    return response
