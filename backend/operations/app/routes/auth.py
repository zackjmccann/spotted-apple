"""
Routes at the auth url prefix are dedicated to communication with the Authentication Server
"""
from flask import Blueprint, request
from services.auth import authenticate_with_auth_server, AuthenticationError


auth = Blueprint('auth', __name__)

auth_cors_config = {
    r'/*': {
        'origins': 'http://localhost:3000',
        'methods': ['GET', 'POST', 'OPTIONS'],
        'allow_headers': ["Authorization", "Content-Type"],
        'supports_credentials': True
        }
    }

@auth.route('/login', methods=['POST'])
def login():
    try:
        # TODO: Build login flow:
        # 1. Accept credentials from client
        # 2. Perform payload/request validation
        # 3. Redirect to auth server
        # 4. Receive auth code from auth server
        # 5. Exchange auth code for tokens
        # 6. Respond back to client with tokens

        # The only responses that should come from this function
        # are errors. Otherwise, the request to this endpoint is
        # redirected to the auth service, which responds to the
        # /auth/callback endpoint.

        # Any failure here raises an AuthenticationError
        response = authenticate_with_auth_server(request) 
        return response

    except AuthenticationError:
        return {
            'code': 469,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authorization request',
            }
        }

@auth.route('/callback', methods=['GET'])
def callback():
    parameters = {
            'code': request.args.get('code'),
            'state': request.args.get('state'),
        }
    return {
        'code': 200,
        'data': {
            'status': 'Sucesss',
            'parameters': parameters,
            }
        }