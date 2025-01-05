auth_code_payload_schema = {
    'title' : 'Authentication Code Exchange Request Payload',
    'description': 'Expected payload for an authentication code exchange request',
    'type': 'object',
    'properties': {
        'client_id': { 'type': 'string', 'minLength': 1 },
        'client_secret': { 'type': 'string', 'minLength': 1 },
        'session': { 'type': 'string', 'minLength': 1 },
        'code': { 'type': 'string', 'minLength': 1 },
        'grant_type': { 'type': 'string', 'pattern': '^authentication_code$' },
    },
    'required': ['client_id', 'client_secret', 'session', 'code', 'grant_type',],
}
