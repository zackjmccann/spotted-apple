from services.auth import validate_token
from utilities import BackendResponse
from werkzeug.wrappers import Request


class Authenticator:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app
    
    def __call__(self, environment, start_response):
        request = Request(environment)

        if request.path[:5] == '/auth' or request.method == 'OPTIONS':
            return self.wsgi_app(environment, start_response)

        token = None

        if 'Authorization' not in request.headers:
            return BackendResponse({
                'code': 400,
                'data': {
                    'status': 'Failed',
                    'message': 'Authorizaiton Header missing'
                    }
            })(environment, start_response)

        token = request.headers['Authorization'].split(" ")[1]
        response = validate_token(token)

        if not response['valid']:
            return BackendResponse({
                'code': response['code'],
                'data': {
                    'status': response['status'],
                    'message': response['message'],
                    }
            })(environment, start_response)

        return self.wsgi_app(environment, start_response)
