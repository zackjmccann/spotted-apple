from flask import Blueprint, request, make_response
from urllib.parse import urlencode
from werkzeug.utils import redirect
from werkzeug.exceptions import UnsupportedMediaType
from services.auth import (
    authenticate,
    validate_token,
    issue_token,
    set_cookies,
    is_blacklisted_token,
    blacklist_token,
    parse_token,
    get_authorization_code,
    AuthenticationError
    )

auth = Blueprint('auth', __name__)

@auth.route('/token', methods=["POST"])
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

@auth.route('/authorize', methods=['GET'])
def authorize():
    try:
        payload = {
            'email': request.args.get('email'),
            'password': request.args.get('password'),
            'grant_type': request.args.get('grant_type'),
        }

        parameters = {
            'client_id': request.args.get('client_id'),
            'redirect_uri': request.args.get('redirect_uri'),
            'state': request.args.get('state'),
            'response_type': request.args.get('response_type'),
            'scope': request.args.get('scope'),
            'code_challenge': request.args.get('code_challenge'),
            'code_challenge_method': request.args.get('code_challenge_method'),
        }

        # Any failure here raises an AuthenticationError
        authorization_code = get_authorization_code(payload, parameters)
        redirect_uri = parameters['redirect_uri']
        query_parameters = {
            'code': authorization_code,
            'state': parameters['state']
        }
        params = urlencode(query_parameters)
        return redirect(location=f'{redirect_uri}?{params}', code=302)

    except (TypeError, KeyError, UnsupportedMediaType, AuthenticationError):
        return {
            'code': 405,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authorization request',
            }
        }
