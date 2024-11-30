import os
import jwt
import datetime
from werkzeug.wrappers import Request, Response
from spotted_apple_logging import logger


def issue_token(username):
    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('JWT_ALORITHM')
    app_id = os.getenv('APP_ID')

    data = {
        'iss': 'spotted-apple-backend',
        'aud': app_id,
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
        'jti': 'backend_services' + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M'),
        'context': {
            'username': username,
            'roles':['client']
            }
        }

    return jwt.encode(data, secret_key, algorithm)


class Authenticator:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app
    
    def __call__(self, environment, start_response):
        request = Request(environment)

        if request.path == '/auth/':
            return self.wsgi_app(environment, start_response)

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return Response('Missing token', status=401)(environment, start_response)

        try:
            secret_key = os.getenv('SECRET_KEY')
            algorithms = [os.getenv('JWT_ALORITHM')]
            app_id = os.getenv('APP_ID')
            jwt.decode(token, secret_key, algorithms=algorithms, audience=app_id)
            logger.info('Token validated.')

        except jwt.ExpiredSignatureError:
            return Response('Expire token', status=401)(environment, start_response)
        
        except jwt.InvalidTokenError:
            return Response('Invalid token', status=401)(environment, start_response)

        return self.wsgi_app(environment, start_response)
