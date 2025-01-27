from app.models import (
    middleware_client,
    auth_login,
    token_introspect,
    token_revoke,
    )

schemas = {
    'middleware_client': middleware_client.schema,
    'auth_login': auth_login.schema,
    'token_introspect': token_introspect.schema,
    'token_revoke': token_revoke.schema,
}

type_mappings = {
    'middleware_client': middleware_client.type_mappings,
    'auth_login': auth_login.type_mappings,
    'token_introspect': token_introspect.type_mappings,
    'token_revoke': token_revoke.type_mappings,
}


__all__ = ['schemas', 'type_mappings']
