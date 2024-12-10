from flask import Blueprint, request
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
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email', None)
            assert email is not None
        else:
            return { 'code': 200, 'data': {} }

    except (UnsupportedMediaType, AssertionError):
        return {
            'code': 400,
            'data': {
                'ok': False,
                'status': 'failed',
                'message': 'Bad request: did not contain an email or not json content type',
            }
        }

    return {
        'code': 200,
        'data': {
            'ok': True,
            'registered': email_is_registered(email), 
            }
        }
