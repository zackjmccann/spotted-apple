from jsonschema import ValidationError
from flask import current_app, request, Blueprint
from werkzeug.exceptions import UnsupportedMediaType
from utilities.payload_handler import PayloadHandler
from services.errors import AuthenticationError, TokenError

token = Blueprint('token', __name__)

@token.route('/introspect', methods=['POST'])
def introspect():
    """Introspect JWT token"""
    try:
        payload = PayloadHandler(request.get_json(), request.path)

        token_validity = current_app.token_service.validate_token(payload.data.get('token'))
        return {'valid': token_validity}, 200

    except (KeyError, ValidationError, UnsupportedMediaType, AuthenticationError, TokenError):
        return {'valid': False}, 200

@token.route('/revoke', methods=['POST'])
def revoke():
    """Revoke JWT token"""
    try:
        payload = PayloadHandler(request.get_json(), request.path)

        token_revoked = current_app.token_service.revoke_token(payload.data.get('token'))
        return {'revoked': token_revoked}, 200

    except (KeyError, ValidationError, UnsupportedMediaType, AuthenticationError, TokenError):
        return {'revoked': False}, 200
