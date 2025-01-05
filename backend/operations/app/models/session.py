session_payload_schema = {
    'title' : 'Session Validation Request',
    'description': 'Expected payload for a session validation request',
    'type': 'object',
    'properties': {
        'session': { 'type': 'string', 'minLength': 1 },
        'client_id': { 'type': 'string', 'minLength': 1 },
    },
    'required': ['session', 'client_id'],
}

session_schema = {
    'title' : 'Client Session',
    'description': 'Expected structure of a client session',
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer'},
        'session_id': {'type': 'string', 'minLength': 1 },
        'created_at': {'type': 'datetime' },
        'expires_at': {'type': 'datetime' },
        'client_id': {'type': 'string', 'minLength': 1 },
    },
    'required': ['id', 'session_id', 'created_at', 'expires_at', 'client_id',],
}

