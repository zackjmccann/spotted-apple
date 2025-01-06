from app.models import auth_authenticate_service

schemas = {
    'auth_authenticate_service': auth_authenticate_service.schema,
}

type_mappings = {
    'auth_authenticate_service': auth_authenticate_service.type_mappings,
}


__all__ = ['schemas', 'type_mappings']
