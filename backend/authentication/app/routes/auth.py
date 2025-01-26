from jsonschema import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from flask import current_app, request, Blueprint
from utilities.payload_handler import PayloadHandler
from services.errors import AuthenticationError, TokenError
from flask import current_app

auth = Blueprint('auth', __name__)

@auth.route('/authenticate/service', methods=['POST'])
def authenticate_service():
    """
    Authorize a service to interact with the Spotted Apple Authentication Server

    Service are registered to interact with this server, and must present a
    valid token in all request outside this route. This is the only entry point
    to be issued a token.

    Expected payloads delivered to this endpoint must present the following:
        Service ID     : The unique ID of the service requesting authentication
        Service Name   : The name associated with the service during onbaording
        Service Secret : A secret key issued by the auth server during onboarding (associated with the service ID)
        Grant Type     : Only "client_credentials" is accepted

    """
    try:
        payload = PayloadHandler(request.get_json(), request.path)

        authenticated = current_app.auth_service.authenticate_service(payload.data)
        
        if authenticated:
            tokens = current_app.token_service.issue_service_tokens(payload.data)
            return tokens, 200

    except (KeyError, ValidationError, UnsupportedMediaType, AuthenticationError, TokenError):
        return {'message': 'Failed to authenticate.'}, 400


@auth.route('/authenticate/client', methods=['POST'])
def authenticate_client():
    """
    Authorize a Client to interact with the Spotted Apple Backend

    Clients only communicate with the Ops Server, but are authenticated via
    the Auth Server. As in, when a client requests data from the Ops server, it
    must present the server with data for an active session, which is only provided
    if the client has been authenticated.

    Clients are registered with the Authenticatation server, and validated via this
    endpoint. Services are able to present authentication data with a valid token present
    in the Authorization header, which they recieve by first authenticating themselves. The
    client data is then validated and authentication is determined.

    Expected payload delivered to this endpoint much present the following:
        Client ID       : The ID of the client requesting to create a session
        Client Username : The name of the client
        Client Secret   : A secret key associated with the client ID
        Grant Type      : Only "client_credentials" is accepted
    """
    return {'text': 'some text', 'values': 'some value'}, 200
