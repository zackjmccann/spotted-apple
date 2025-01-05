from flask import Blueprint, request

auth = Blueprint('auth', __name__)

@auth.route('/authorize/client', methods=['POST'])
def authorize_client():
    """
    Authorize a client to interact with the Spotted Apple Backend

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
    return {'code': 200, 'data': {'authorized': True}}
