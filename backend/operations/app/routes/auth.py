"""
Routes at the auth url prefix are dedicated to communication with the Authentication Server
"""
from flask import Blueprint, request
from services.auth import (
    authenticate_with_auth_server,
    authenticate_user_account,
    exchange_code_for_tokens,
    create_session,
    validate_session,
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
    # try:
    #     # Any failure here raises an AuthenticationError
    #     response = authenticate_with_auth_server(request)
    #     if response.status_code == 200:
    #         data = response.json()
    #         return {'code': 200, 'data': data}

    # except AuthenticationError:
    #     return {
    #         'code': 405,
    #         'data': {
    #             'status': 'Failed',
    #             'message': 'Unable to process authorization request',
    #         }
    #     }
    try:
        data = request.get_json()
        auth_data = authenticate_user_account(data)
        return {'code': 200, 'data': auth_data} # {code: ... state: ...}
    
    except AuthenticationError:
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Unable to process authentication request'
            }
        }

@auth.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code', None)
    state = request.args.get('state', None)
    try:
        assert code is not None
        assert state is not None # TODO: Verify state is truly echoed (should be found in the cookie)

        # TODO: Any failure here raises an AuthenticationError

        # Exchange token will ultimately call /auth/token on OAuth server. The following need
        # to be in the payload:
            # code
            # client_id
            # client_secret
            # code_verifier
            # grant_type
            # redirect_uri
        tokens = exchange_code_for_tokens(code, state)

        return {
            'code': 200,
            'data': {
                'status': 'Sucesss',
                'id_token': tokens['id'],
                'access_token': tokens['access'],
                'refresh_token': tokens['refresh'],
                }
            }
    except (AssertionError, AuthenticationError):
        raise AuthenticationError('Authentication failed')

@auth.route('/token', methods=['GET'])
def token():
    """
    TODO: Include the following in payload
    code          : this is the authorization code we are exchanging for tokens.
    client_id     : this identifies our application. In FusionAuth it is a UUID, but it could be any URL safe string.
    client_secret : this is a secret key that is provided by the OAuth server. This should never be made public and should only ever be stored in your application on the server.
    code_verifier : this is the code verifier value we created above and either stored in the session or in a cookie.
    grant_type    : this will always be the value authorization_code to let the OAuth server know we are sending it an authorization code.
    redirect_uri  : this is the redirect URI that we sent to the OAuth server above. It must be exactly the same value.
    """
    return {
        'code': 200,
        'data': {
            'status': 'Sucesss',
            'parameters': 'parameters',
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
