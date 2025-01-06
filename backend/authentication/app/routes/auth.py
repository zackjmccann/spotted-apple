from jsonschema import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from flask import current_app, request, jsonify, Blueprint
from utilities.payload_handlers import Payload
from services import auth_service, token_service


auth = Blueprint('auth', __name__)

@auth.route('/authenticate/service', methods=['POST'])
def authenticate_service():
    """
    Authorize a service to interact with the Spotted Apple Authentication Server

    Service are registered to interact with this server, and must present a
    valid token in all request outside this route. This is the only entry point
    to be issued a token.

    Expected payload delivered to this endpoint much present the following:
        Service ID     : The ID of the service facilitating the client authentication
        Service Secret : A secret key, register with the auth server, associated with the service ID
        Grant Type     : Only "client_credentials" is accepted

    """
    try:
        payload = Payload(request.get_json(), request.path)

        if current_app.auth_service.authenticate_service(payload.data):
            tokens = current_app.token_service.issue_service_tokens(payload.data)
        return tokens, 200
    except (ValidationError, UnsupportedMediaType): # AuthenticationError, TokenError
        return {'message': 'Failed to authenticate.'}, 400


@auth.route('/authenticate/client', methods=['POST'])
def authenticate_client():
    """
    Authorize a Client to interact with the Spotted Apple Backend

    Clients only communicate with the Ops Server, but are authenticated via
    the Auth Server. As in, when a client requests data from the Ops server, it
    must present data for an active session, which is only provided if the client has been
    authenticated.

    Clients are registered with the Authenticatation server, and validated via this
    endpoint. Only permitted services (e.g., the Ops Server) are granted permission
    to present authentication data, and from there, the data is validateed and authorization
    is determined.

    Expected payload delivered to this endpoint much present the following:
        Service ID      : The ID of the service facilitating the client authentication
        Service Secret  : A secret key, register with the auth server, associated with the service ID
        Client ID       : The ID of the client requesting to create a session
        Client Username : The name of the client
        Client Secret   : A secret key associated with the client ID
        Grant Type      : Only "client_credentials" is accepted

    """
    current_app.logger.info(f'Fielding request to /auth/authorize/client...')
    rows = current_app.db.execute_query(
        {'text':'SELECT * FROM clients;', 'values': {}},
        return_method='fetchall',
        cursor_type='RealDictCursor')
    return jsonify(rows), 200
