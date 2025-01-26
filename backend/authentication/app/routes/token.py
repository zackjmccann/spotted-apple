from jsonschema import ValidationError
from flask import current_app, request, Blueprint
from werkzeug.exceptions import UnsupportedMediaType
from utilities.payload_handler import PayloadHandler
from services.errors import AuthenticationError, TokenError

token = Blueprint('token', __name__)

@token.route('/introspect', methods=['POST'])
def introdpect_token():
    """Introspect a payload for a valid token?"""
    try:
        payload = PayloadHandler(request.get_json(), request.path)

        # TODO: validate_token is not expecting a payload
        valid = current_app.auth_service.validate_token(payload.data)
        
        if valid:
            return {'valid': True}, 200

    except (KeyError, ValidationError, UnsupportedMediaType, AuthenticationError, TokenError):
        return {'valid': False}, 200
