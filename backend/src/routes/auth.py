from flask import Blueprint, request
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
                    'status': response['status'],
                    'message': response['message'],
            }
        }
    
        token = issue_token(data.get('username'), data.get('id'))

        return {
            'code': 200,
            'data': {
                'status': 'Access Granted',
                'token': token,
                }
            }

    except (TypeError, KeyError):
        return {
            'code': 400,
            'data': {
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
                    'status': response['status'],
                    'message': response['message'],
                    }
            }

        else:
            return {'code': 201, 'data': {'valid': True}}

    except (TypeError, AttributeError):
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authorization request'
                },
        }
