from app.models import (
    auth_authenticate_service,
    auth_login,
    middleware_client)

schemas = {
    'auth_authenticate_service': auth_authenticate_service.schema,
    'auth_login': auth_login.schema,
    'middleware_client': middleware_client.schema,
}

type_mappings = {
    'auth_authenticate_service': auth_authenticate_service.type_mappings,
    'auth_login': auth_login.type_mappings,
    'middleware_client': middleware_client.type_mappings,
}


__all__ = ['schemas', 'type_mappings']
