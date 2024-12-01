import os
import jwt
import json
import datetime
from database.aloe import Aloe
from werkzeug.wrappers import Request, Response
from spotted_apple_logging import logger


def authenticate_with_database(credentials):
    aloe = Aloe()
    response =  aloe.authenticate_client(credentials)

    if not response['valid']:
        response.update({
            'message': 'authentication failed',
            'status': 401,
            'content_type': 'application/json',
        })

    return response

def issue_token(username, id):
    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('JWT_ALORITHM')

    data = {
        'iss': 'spotted-apple-backend',
        'aud': [str(id)],
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
        'jti': 'backend_services' + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M'),
        'context': {
            'username': username,
            'roles':['client']
            }
        }

    return jwt.encode(data, secret_key, algorithm)

def validate_token(token):
    logger.info(f'token: {token}')
    if not token:
        return {
            'valid': False,
            'message': 'unable to process authorization request',
            'status': 400,
            'content_type': 'application/json',
            }

    secret_key = os.getenv('SECRET_KEY')
    algorithms = [os.getenv('JWT_ALORITHM')]
    app_id = os.getenv('APP_ID') # TODO: Change to array of authorized apps?

    try:
        data = jwt.decode(token, secret_key, algorithms=algorithms, audience=app_id)
        data.update({'valid': True})
        return data

    except jwt.ExpiredSignatureError:
        message = {
            'status': 'Authentication Failed',
            'message': 'Token Expired'
            }
        status = 401
        content_type = 'application/json'

    except jwt.InvalidTokenError:
        message = {
            'status': 'Authentication Failed',
            'message': 'Invalid Token'
            }
        status = 401
        content_type = 'application/json'

    return {
        'valid': False,
        'message': message,
        'status': status,
        'content_type': content_type,
        }

class Authenticator:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app
    
    def __call__(self, environment, start_response):
        request = Request(environment)

        if request.path[:5] == '/auth':
            return self.wsgi_app(environment, start_response)

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            message = {
                'status': 'Authentication Failed',
                'message': 'Missing Token'
                }
            status = 401
            content_type = 'application/json'
            return Response(
                response=json.dumps(message),
                status=status,
                content_type=content_type)(environment, start_response)

        response = validate_token(token)

        if not response['valid']:
            return Response(
                response=json.dumps(response['message']),
                status=response['status'],
                content_type=response['content_type'])(environment, start_response)

        return self.wsgi_app(environment, start_response)
