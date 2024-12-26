from flask import Blueprint, request, make_response
from services.auth import (
    authenticate,
    validate_token,
    issue_token,
    set_cookies,
    is_blacklisted_token,
    blacklist_token,
    parse_token,
    )

auth = Blueprint('auth', __name__)

@auth.route('/token', methods=['POST'])
def get_token():
    try:
        data = request.get_json()
        response = authenticate(data)

        if not response['valid']:
            return {
                'code': response['code'],
                'data': {
                    'status': response['status'],
                    'message': response['message'],
            }
        }
    
        access_token = issue_token(response.get('username'), response.get('id'), 10)
        refresh_token = issue_token(response.get('username'), response.get('id'), 10080) # 7 days
        response_data = {
            'code': 200,
            'data': {
                'status': 'Access Granted',
                'access_token': access_token,
                'refresh_token': refresh_token,
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
                'status': 'Failed',
                'message': 'Unable to process authorization request',
            }
        }

@auth.route('/introspect', methods=['POST'])
def introspect_token():
    try:
        data = request.get_json()
        response = validate_token(data.get('access_token', None))

        if not response['valid']:
            return {
                'code': response['code'],
                'data': {
                    'status': response['status'],
                    'message': response['message'],
                    }
            }

        else:
            return {'code': 200, 'data': {'valid': True}}

    except (TypeError, AttributeError):
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authorization request'
                },
        }

@auth.route('/refresh', methods=['POST'])
def refresh_token():
    try:
        data = request.get_json()
        refresh_token = str(data.get('refresh_token', None))
        assert not is_blacklisted_token(refresh_token)
        response = validate_token(refresh_token)
        if not response['valid']:
            return {
                'code': response['code'],
                'data': {
                    'status': response['status'],
                    'message': response['message'],
                    }
            }

        else:
            refresh_token_response = blacklist_token(refresh_token)
            assert refresh_token_response['code'] == 200

            refresh_token_data = parse_token(refresh_token)    
            username = refresh_token_data['context']['username']
            id = refresh_token_data['aud'][0]
            access_token = issue_token(username, id, 10)
            refresh_token = issue_token(username, id, 10080) # 7 days
            response_data = {
                'code': 200,
                'data': {
                    'status': 'Tokens refreshed',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    }
                }

            response = make_response(response_data)
            set_cookies(response, [
                {'type': 'access_token', 'token': access_token},
                {'type': 'refresh_token', 'token': refresh_token},
                ])

            return response

    except (TypeError, AttributeError, AssertionError):
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process token refresh request'
                },
        }

@auth.route('/revoke', methods=['POST'])
def revoke_token():
    try:
        data = request.get_json()
        token = str(data.get('token', None))
        response = validate_token(token)
        if not response['valid']:
            return {
                'code': response['code'],
                'data': {
                    'status': response['status'],
                    'message': response['message'],
                    }
            }
        blacklist_response = blacklist_token(token)
        assert blacklist_response['code'] == 200
        return {
            'code': 200,
            'data': { 
                'status': 'Success',
                'message': 'Token blacklisted'
            }
        }

    except (TypeError, AttributeError, AssertionError):
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process token blacklist request'
                },
        }
