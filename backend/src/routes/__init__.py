from src.routes.api import api, api_cors_config
from src.routes.auth import auth
from src.routes.test import test_bp
from src.routes.user import user

blueprints = [
    {'blueprint': api, 'url_prefix': '/api', 'cors_config': api_cors_config},
    {'blueprint': auth, 'url_prefix': '/auth'},
    {'blueprint': test_bp, 'url_prefix': '/test'},
    {'blueprint': user, 'url_prefix': '/user'},
]

__all__ = [
    'blueprints',
]