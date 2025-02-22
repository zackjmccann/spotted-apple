from flask import Flask
from app.services.base_service import BaseService
from app.services.auth_service import AuthenticationService
from app.services.token_service import TokenService

def init_app(app: Flask):
    app.logger.debug('Initializing services...')
    app.auth_service = AuthenticationService(app)
    app.token_service = TokenService(app)


__all__ = [
    'init_app'
]
