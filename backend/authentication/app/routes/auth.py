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
        Grant Type    : Only "authorization" is accepted
        Email         : The email attempting to authenticate
        Password      : The password associated with the provided username

    A client ID and name are required to create access tokens. These are parsed
    from the request headers, which are validated by the Midddleware, so they
    should always be present.
    """
    try:
        payload = PayloadHandler(request.get_json(), request.path)

        authenticated = current_app.auth_service.authenticate_user(payload.data)

        if authenticated:
            user_data = payload.data
            user_data.update({
                'client_id': request.headers.get('Client-ID'),
                'client_name': request.headers.get('Client-Name'),
            })
            tokens = current_app.token_service.issue_user_access_tokens(user_data)
            return tokens, 200

    except (KeyError, ValidationError, UnsupportedMediaType, AuthenticationError, TokenError):
        return {'message': 'Failed to authenticate.'}, 400
