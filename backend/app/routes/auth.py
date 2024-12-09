from flask import Blueprint, request, make_response
from services.auth import authenticate, validate_token, issue_token
from werkzeug.exceptions import UnsupportedMediaType

auth = Blueprint('auth', __name__)

@auth.route('/token', methods=["POST"])
def get_token():
    try:
        data = request.get_json()

        if data['grant_type'] == 'client_credentials':
            client_credentials = {
                'username': data.get('username', None),
                'password': data.get('password', None),
                'id': data.get('id', None),
                }

            response = authenticate(client_credentials)

        elif data['grant_type'] == 'refresh_token':
            response = validate_token(data.get('refresh_token', None))


        if not response['valid']:
            return {
                'code': response['code'],
                'data': {
                    'ok': False,
                    'status': response['status'],
                    'message': response['message'],
            }
        }
    
        token = issue_token(data.get('username'), data.get('id'))
        response_data = {
            'code': 200,
            'data': {
                'ok': True,
                'status': 'Access Granted',
                'token': token,
                }
            }
        
        response = make_response(response_data)
        response.set_cookie(
            'token',
            token,
            httponly=True,
            secure=False,  # Use True when app is using HTTPS
            samesite='Strict',
            max_age=24 * 60 * 60  # Token valid for 1 day
        )
        return response

    except (TypeError, KeyError):
        return {
            'code': 400,
            'data': {
                'ok': False,
                'status': 'Failed',
                'message': 'Unable to process authorization request',
            }
        }

@auth.route('/introspect', methods=['POST'])
def introspect_token():
    try:
        data = request.get_json()
        response = validate_token(data.get('token', None))

        if not response['valid']:
            return {
                'code': response['code'],
                'data': {
                    'ok': False,
                    'status': response['status'],
                    'message': response['message'],
                    }
            }

        else:
            return {'code': 200, 'data': {'ok': True, 'valid': True}}

    except (TypeError, AttributeError):
        return {
            'code': 400,
            'data': {
                'ok': False,
                'status': 'Failed',
                'message': 'Unable to process authorization request'
                },
        }
