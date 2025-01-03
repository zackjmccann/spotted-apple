"""
Routes at the auth url prefix are dedicated to communication with the Authentication Server
"""
from flask import Blueprint, request
from services.auth import (
    create_session,
    validate_session,
    authenticate_user_account,
    exchange_authentication_code,
    AuthenticationError,
    )


auth = Blueprint('auth', __name__)

auth_cors_config = {
    r'/*': {
        'origins': 'http://localhost:3000',
        'methods': ['GET', 'POST', 'OPTIONS'],
        'allow_headers': ["Authorization", "Content-Type"],
        'supports_credentials': True
        }
    }

@auth.route('/session/create', methods=['POST'])
def session_create():
    """
    Create a session for the frontend.

    Session are created for known, authenticated clients. First, a client
    is authenticated against a clients table in the database. If authenticated,
    a session is created and returned to the client. By default, sessions expire
    5 minutes after creation. Clients can re-authenticate in order to persist
    sessions.
    """
    try:
        data = request.get_json()
        session = create_session(data)
        return {'code': 200, 'data': session}
    except AuthenticationError:
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to create or get session',
            }
        }

@auth.route('/session/introspect', methods=['POST'])
def session_validate():
    try:
        data = request.get_json()
        if validate_session(data):
            return {'code': 200, 'data': {'valid': True}}
        else:
            raise AuthenticationError
    except AuthenticationError:
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to create or get session',
            }
        }

@auth.route('/login', methods=['POST'])
def login():
    """
    The entry point for user account login and authenticatation with the Authentication Service.

    Clients are responsible for providing the following:
        - Client ID:
            The client ID of the Authentication Service
        - Client Secret:
            A secret, provided by the Authentication Service
        - Session Id:
            The id of the current session. The session will be validated first, then
            the state will be extracted and sent to the authentication service, which
            will echo back the value.

        TODO: Implement the following?
        - Code Challenge:
            A value which will be collected and stored by the Authentication Service to
            validate subsequent request from a given client.
    """
    try:
        data = request.get_json()
        auth_data = authenticate_user_account(data)
        return {'code': 200, 'data': auth_data}

    except AuthenticationError:
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authentication request'
            }
        }

@auth.route('/token/exchange', methods=['POST'])
def token():
    """
    Exchange an authentication code for access tokens.
        code          : this is the authorization code we are exchanging for tokens.
        client_id     : this identifies our application. In FusionAuth it is a UUID, but it could be any URL safe string.
        client_secret : this is a secret key that is provided by the OAuth server. This should never be made public and should only ever be stored in your application on the server.
        grant_type    : this will always be the value authorization_code to let the OAuth server know we are sending it an authorization code.
    
    TODO: Include the following in payload
        code_verifier : this is the code verifier value we created above and either stored in the session or in a cookie.
    """
    try:
        data = request.get_json()
        tokens = exchange_authentication_code(data)
        return {'code': 200, 'data': tokens}

    except AuthenticationError:
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authentication request'
            }
        }
