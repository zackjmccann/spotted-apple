from werkzeug.wrappers import Request
from utilities import BackendResponse
from services.auth import validate_authorization_token


class Authenticator:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app
    
    def __call__(self, environment, start_response):
        request = Request(environment)

        if 'Authorization' not in request.headers:
            return BackendResponse({
                'code': 400,
                'data': {
                    'status': 'Failed',
                    'message': 'Authorizaiton Header missing'
                    }
            })(environment, start_response)

        response = validate_authorization_token(request)

        if not response['valid']:
            return BackendResponse({
                'code': response['code'],
                'data': {
                    'status': 'Failed',
                    'message': 'Unauthorized'
                    }
            })(environment, start_response)

        return self.wsgi_app(environment, start_response)
