from flask import Blueprint, request, make_response
from urllib.parse import urlencode
from werkzeug.utils import redirect
from werkzeug.exceptions import UnsupportedMediaType
from services.auth import (
    authenticate_client,
    get_authorization_code,
    exchange_auth_code_for_tokens,
    validate_token,
    issue_token,
    set_cookies,
    is_blacklisted_token,
    blacklist_token,
    parse_token,
    AuthenticationError
    )

auth = Blueprint('auth', __name__)

@auth.route('/authorize/client', methods=['POST'])
def authorize_client():
    try:
        payload = request.get_json()
        response = authenticate_client(payload)
        if not response['valid']:
            raise AuthenticationError
        return {'code': 200, 'data': {'authorized': True}}
    except (TypeError, KeyError, UnsupportedMediaType, AuthenticationError):
        return {
            'code': 401,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authorization request',
            }
        }

@auth.route('/authorize/user', methods=['POST'])
def authorize_user():
    try:
        payload = request.get_json()
        auth_code = get_authorization_code(payload)
        state = payload.get('state', None)
        
        if not state:
            raise AuthenticationError
        
        return {
            'code': 200,
            'data': { 'code': auth_code, 'state': state, },
            }

    except (TypeError, KeyError, UnsupportedMediaType, AuthenticationError):
        return {
            'code': 401,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authorization request',
            }
        }

@auth.route('/token', methods=["POST"])
def get_token():
    try:
        data = request.get_json()
        response = exchange_auth_code_for_tokens(data)

        if not response['valid']:
            raise AuthenticationError
    
        test_token = issue_token('test', 'testId', 10)
        # access_token = issue_token(response.get('username'), response.get('id'), 10)
        # refresh_token = issue_token(response.get('username'), response.get('id'), 10080) # 7 days
        return {
            'code': 200,
            'data': {
                'id_token': test_token,
                'access_token': test_token,
                'refresh_token': test_token,
                }
            }
    except (TypeError, KeyError, AuthenticationError):
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
