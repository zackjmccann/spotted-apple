from app.routes.auth import auth
from app.routes.token import token

blueprints = [
    {'blueprint': auth, 'url_prefix': '/auth'},
    {'blueprint': token, 'url_prefix': '/token'},
]

__all__ = [
    'blueprints',
]