from jsonschema import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from flask import current_app, request, Blueprint
from utilities.payload_handler import PayloadHandler
from services.errors import AuthenticationError, TokenError
from flask import current_app

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    """
    Authenticate an application user.

    Expected payload delivered to this endpoint much present the following:
        Client ID     : The ID of the client facilitating the authentication
        Client Name   : The name of the client facilitating the authentication
        Client Secret : A secret key associated with the client
        Grant Type    : Only "authorization" is accepted
        Email         : The email attempting to authenticate
        Password      : The password associated with the provided username
    """
    try:
        payload = PayloadHandler(request.get_json(), request.path)

        authenticated = current_app.auth_service.authenticate_user(payload.data)

        if authenticated:
            tokens = current_app.token_service.issue_user_access_tokens(payload.data)
            return tokens, 200

    except (KeyError, ValidationError, UnsupportedMediaType, AuthenticationError, TokenError):
        return {'message': 'Failed to authenticate.'}, 400
