from app.services import BaseService
from services.errors import AuthenticationError


class AuthenticationService(BaseService):
    def __init__(self, app):
        super().__init__(app)

    def authenticate_user(self, payload: dict) -> bool:
        """Authenticate an application user"""
        response = self.app.db.authenticate_user(payload)
        if not response['valid']:
            raise AuthenticationError
        return True
