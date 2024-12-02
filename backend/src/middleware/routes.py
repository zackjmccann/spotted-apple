from flask import Blueprint, request, jsonify
from middleware.auth import issue_token, validate_token, authenticate_with_database


auth_blueprint = Blueprint('auth', __name__)

class AuthenticationException(BaseException):
    pass

@auth_blueprint.route('/token', methods=['POST'])
def get_token():
    try:
        data = request.get_json()

        if data['grant_type'] == 'client_credentials':
            client_credentials = {
                'username': data.get('username', None),
                'password': data.get('password', None),
                'id': data.get('id', None),
                }
            response = authenticate_with_database(client_credentials)

        elif data['grant_type'] == 'refresh_token':
            response = validate_token(data.get('refresh_token', None))

        else:
            response = {'valid': False}

        if not response['valid']:
            return jsonify({
                'status': 'failed',
                'message': response['message']
                }), response['status']

        token = issue_token(response['username'], response['id'])
        
        return jsonify({
            'status': 'success',
            'message': 'Access Granted',
            'token': token
            }), 200

    except (TypeError, KeyError):
        return jsonify({
            'status': 'failed',
            'message': 'unable to process authorization request'
            }), 400

@auth_blueprint.route('/introspect', methods=['POST'])
def introspect_token():
    try:
        data = request.get_json()
        response = validate_token(data.get('token', None))
        if not response['valid']:
            return jsonify({ 'valid': False, }), 201
        else:
            return jsonify({ 'valid': True, }), 201
    except (TypeError, AttributeError):
        return jsonify({
            'status': 'failed',
            'message': 'unable to process authorization request'
            }), 400