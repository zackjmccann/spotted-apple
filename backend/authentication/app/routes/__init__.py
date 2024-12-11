from app.routes.auth import auth
from app.routes.register import register

blueprints = [
    {'blueprint': auth, 'url_prefix': '/auth'},
    {'blueprint': register, 'url_prefix': '/register'},
]

__all__ = [
    'blueprints',
]