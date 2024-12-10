from app.routes.auth import auth

blueprints = [
    {'blueprint': auth, 'url_prefix': '/auth'},
]

__all__ = [
    'blueprints',
]