from flask import Blueprint, request
from services.auth import AuthenticationError
from services.api import email_is_registered
from werkzeug.exceptions import UnsupportedMediaType

api = Blueprint('api', __name__)

api_cors_config = {
    r'/*': {
        'origins': 'http://localhost:3000',
        'methods': ['GET', 'POST', 'OPTIONS'],
        'allow_headers': ["Authorization", "Content-Type"],
        'supports_credentials': True
        }
    }

@api.route('/check-email', methods=['POST', 'OPTIONS'])
def check_email():
    try:
        # UnsupportedMediaType is raised if request content type is not 'application/json'
        data = request.get_json()
        email = data.get('email', None)
        assert email is not None

    except (UnsupportedMediaType, AssertionError):
        return {
            'code': 400,
            'data': {
                'status': 'failed',
                'message': 'Bad request: did not contain an email or not json content type',
            }
        }

    try:
        is_registered = email_is_registered(email, request.headers)
        code = 200
        data = {
            'status': 'success',
            'registered': is_registered,
            }

    except AuthenticationError as err:
        code = err.code
        data = {
            'status': err.status,
            'message': str(err),
            }

    return {'code': code, 'data': data}
