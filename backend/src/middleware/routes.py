from flask import Blueprint, request, jsonify
from database.aloe import Aloe
from middleware.auth import issue_token

auth_blueprint = Blueprint('auth', __name__)
aloe = Aloe()

@auth_blueprint.route('/', methods=['POST'])
def login():
    client_credentials = {
        'username': request.json.get('username', None),
        'password': request.json.get('password', None),
        'id': request.json.get('id', None),
        }
    response = aloe.client_login(client_credentials)

    if not response['valid']:
        return jsonify({
            'status': 'failed',
            'message': 'unauthorized client'
            }), 401
    
    token = issue_token(client_credentials['username'])
    return jsonify({
        'status': 'success',
        'message': 'Access Granted',
        'access_token': token
        }), 200
