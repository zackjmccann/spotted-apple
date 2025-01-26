from app.services import BaseService
from services.errors import AuthenticationError


class AuthenticationService(BaseService):
    def __init__(self, app):
        super().__init__(app)
        # self.server = self._get_environment_variable('AUTH_SERVER')
        # self.secret = self._get_environment_variable('AUTH_SECRET')
        # self.client_id = self._get_environment_variable('AUTH_CLIENT_ID')

    def authenticate_service(self, payload: dict) -> bool:
        """Authenticate a service"""
        response = self.app.db.authenticate_service(payload)
        if not response['valid']:
            raise AuthenticationError
        return True

    def authenticate_user(self, payload: dict) -> bool:
        """Authenticate an application user"""
        response = self.app.db.authenticate_user(payload)
        if not response['valid']:
            raise AuthenticationError
        return True
