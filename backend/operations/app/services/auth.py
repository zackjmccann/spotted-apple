import os
import requests
import secrets
import hashlib
import base64
from jsonschema import validate, ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from werkzeug.utils import redirect
from urllib.parse import urlencode
from models.login import login_payload_schema


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
    """
    Authentication with AuthService:
    1. Validate request payload
    2. Redirect to authentication server
    3. Field authorization code from auth servers redirect of request back to ops server
    """
    try:
        payload = request.get_json()
        validate(instance=payload, schema=login_payload_schema)
        AUTH_SERVICE = os.getenv('AUTH_SERVICE')

        client_id = APP_ID # TODO: Change this to an actual client id?
        redirect_uri = 'http://localhost:8000/auth/callback' # TODO: Don't hard code this
        state = 'developmentauthstate'
        scopes = 'profile offline_access openid'
        code_challenge = generate_code_challenge(request)

        query_parameters = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': state,
            'response_type': 'code',
            'scope': scopes,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'email': payload.get('email'),
            'password': payload.get('password'),
            'grant_type': payload.get('grant_type'),
        }

        params = urlencode(query_parameters)
        redirect_uri = f'http://{AUTH_SERVICE}/auth/authorize'
        return redirect(location=f'{redirect_uri}?{params}', code=302)

    except (UnsupportedMediaType, ValidationError):
        raise AuthenticationError('Failed to login')

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

def generate_code_challenge(request):
  random_code = secrets.token_urlsafe(96)[:128]
  hashed = hashlib.sha256(random_code.encode('ascii')).digest()
  code_verifier = base64.urlsafe_b64encode(hashed)
#   request.session.oauthCode = code_verifier
  return code_verifier

  # code_challenge = encoded.decode('ascii')[:-1]