from app.routes.api import api, api_cors_config
from app.routes.auth import auth, auth_cors_config
from app.routes.user import user

blueprints = [
    {'blueprint': api, 'url_prefix': '/api', 'cors_config': api_cors_config},
    {'blueprint': auth, 'url_prefix': '/auth', 'cors_config': auth_cors_config},
    {'blueprint': user, 'url_prefix': '/user'},
]

__all__ = [
    'blueprints',
]