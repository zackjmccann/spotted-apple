import os
import jwt
import json
import datetime
from database import aloe

SECRET_KEY = os.getenv('SECRET_KEY')
ALOGRITHMS = os.getenv('JWT_ALORITHM')
APP_ID = os.getenv('APP_ID')
GRANTED_APP_IDS = os.getenv('GRANTED_APP_IDS')

class AuthenticationError(Exception):
    pass

if None in [SECRET_KEY, ALOGRITHMS, APP_ID]:
    raise AuthenticationError('An authentication failure occurred')

def authenticate(credentials):
    response = aloe.authenticate_client(credentials)

    if not response['valid']:
        response.update({
            'code': 401,
            'status': 'Authentication Failed',
            'message': 'Unable to authenticate',
        })

    return response

def issue_token(username, id):
    data = {
        'iss': 'spotted-apple-backend',
        'aud': [str(id)],
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
        'jti': 'backend_services' + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M'),
        'context': {'username': username, 'roles':['client']}
        }

    return jwt.encode(data, SECRET_KEY, ALOGRITHMS)

def validate_token(token):
    print(token)
    if not token:
        return {
            'valid': False,
            'code': 400,
            'status': 'Authentication Failed',
            'message': 'Missing Token',
        }

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=ALOGRITHMS, audience=APP_ID)
        # for aud in data['aud']:
        #     assert aud in GRANTED_APP_IDS

        return {'valid': True, 'code': 200, 'data': data,}

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
