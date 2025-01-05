"""
Routes at the auth url prefix are dedicated to communication with the Authentication Server
"""
from flask import Blueprint, request
from services import (
    auth_service,
    session_service,
    token_service,
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
        clean_payload = auth_service.sanitize_payload(data, 'client')
        if auth_service.authenticate_client(clean_payload):
            client_id = data.get('client_id', None)
            session = session_service.create_session(client_id)
            session_token = token_service.issue_session_token(session)
            return {'session': session_token}, 200
        else:
            raise AuthenticationError
    except AuthenticationError:
        data = {
            'status': 'Failed',
            'message': 'Unable to create or get session',
            }
        return data, 400

@auth.route('/session/introspect', methods=['POST'])
def session_validate():
    """Validate the session within the provided JWT"""
    try:
        data = request.get_json()
        clean_payload = auth_service.sanitize_payload(data, 'session')
        session_token = clean_payload.get('session', None)
        
        if not token_service.validate_token(session_token):
            raise AuthenticationError

        token_data = token_service.decode_token(session_token)
        session_id = token_data['context'].get('id', None)
        
        if session_service.validate_session(session_id):
            return {'valid': True}, 200
        else:
            raise AuthenticationError
    except (AssertionError, AuthenticationError):
        data = {
            'status': 'Failed',
            'message': 'Unable to create or get session',
        }
        return data, 400

@auth.route('/session/revoke', methods=['POST'])
def session_revoke():
    """
    Revoke the session within the provided JWT
    
    A token is first parsed, extracting the session id. If the
    session is not valid, whether expired or no longer in the session
    table, it is assumed that the token has been revoked. The premiss
    being that the provided value is rejected by the server and cannot
    be used as a valid token.
    """
    try:
        data = request.get_json()
        clean_payload = auth_service.sanitize_payload(data, 'session')
        session_token = clean_payload.get('session', None)

        if not token_service.validate_token(session_token):
            raise AuthenticationError

        token_data = token_service.decode_token(session_token)
        session_id = token_data['context'].get('id', None)

        if not session_service.validate_session(session_id):
            return {'revoked': True}, 200
        else:
            if session_service.revoke_session(session_id):
                return {'revoked': True}, 200
            else:
                raise AuthenticationError
    except (AssertionError, AuthenticationError):
        data = {
            'status': 'Failed',
            'message': 'Unable to revoke',
        }
        return data, 400

@auth.route('/login', methods=['POST'])
def login():
    """
    Authentication a user account with the Authentication Service
    
    Clients payloads are validated and sent to the auth service. Payload
    should contain the following:
        client_id     : The client id, which should be registered with the auth service TODO: do we need this?
        client_secret : 
        session       : A JWT containing the client's current session
        email         : Email associated with a user account
        password      : The passowrd associated with the user account
        grant_type    : The grant type for an authentication request
        
    The session value is decoded, extracting the session id which is used to
    validate the session, and extract the session state. The state, along with
    the following fields are added to the payload before sending to the
    authentication service:
        state        : A valid session's associated state, which will be echoed back from the auth service
        response_type: Response type expected from auth service
        scope        : Authentication services scope
        
        TODO: Implement the following?
        code_challenge: A value which will be collected and stored by the Authentication Service to
                        validate subsequent request from a given client.
    """
    try:
        data = request.get_json()
        clean_payload = auth_service.sanitize_payload(data, 'login')
        session_token = clean_payload.get('session', None)

        if not token_service.validate_token(session_token):
            raise AuthenticationError

        token_data = token_service.decode_token(session_token)
        session_id = token_data['context'].get('id', None)

        if not session_service.validate_session(session_id):
            raise AuthenticationError

        session_state = session_service.get_session_state(session_id)
        clean_payload.update({'state': session_state})
        auth_data = auth_service.authenticate_user_account(clean_payload)
        return auth_data, 200

    except AuthenticationError:
        data = {
            'status': 'Failed',
            'message': 'Login Failed',
            }
        return data, 400

@auth.route('/token/exchange', methods=['POST'])
def token():
    """
    Exchange an authentication code for access tokens.
        client_id     : this identifies our application. In FusionAuth it is a UUID, but it could be any URL safe string.
        client_secret : this is a secret key that is provided by the OAuth server. This should never be made public and should only ever be stored in your application on the server.
        session       : A JWT containing the client's current session
        code          : this is the authorization code we are exchanging for tokens.
        grant_type    : this will always be the value authorization_code to let the OAuth server know we are sending it an authorization code.

    The session value is decoded, extracting the session id which is used to
    validate the session, and extract the session state. The state, along with
    the following fields are added to the payload before sending to the
    authentication service:
        state        : A valid session's associated state, which will be echoed back from the auth service
        response_type: Response type expected from auth service

        TODO: Implement the following?
        code_challenge: A value which will be collected and stored by the Authentication Service to
                        validate subsequent request from a given client.
    """
    try:
        data = request.get_json()
        clean_payload = auth_service.sanitize_payload(data, 'auth_code')
        session_token = clean_payload.get('session', None)

        if not token_service.validate_token(session_token):
            raise AuthenticationError

        token_data = token_service.decode_token(session_token)
        session_id = token_data['context'].get('id', None)

        if not session_service.validate_session(session_id):
            raise AuthenticationError

        session_state = session_service.get_session_state(session_id)
        clean_payload.update({'state': session_state})
        auth_data = auth_service.exchange_authentication_code(clean_payload)
        return auth_data, 200

    except AuthenticationError:
        data = {
            'status': 'Failed',
            'message': 'Unable to process authentication request',
            }
        return data, 400
