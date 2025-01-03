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
