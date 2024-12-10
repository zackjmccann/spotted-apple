from flask import Blueprint, request, make_response
from services.auth import authenticate, validate_token, issue_token, set_cookies

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
    
        access_token = issue_token(data.get('username'), data.get('id'), 10)
        refresh_token = issue_token(data.get('username'), data.get('id'), 10080) # 7 days
        response_data = {
            'code': 200,
            'data': {
                'ok': True,
                'status': 'Access Granted',
                'access_token': access_token,
                'refresh': refresh_token,
                }
            }

        response = make_response(response_data)
        set_cookies(response, [
            {'type': 'access_token', 'token': access_token},
            {'type': 'refresh_token', 'token': refresh_token},
            ])

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
