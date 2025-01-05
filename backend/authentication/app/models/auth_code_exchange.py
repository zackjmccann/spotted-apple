auth_code_payload_schema = {
    'title' : 'Authentication Code Exchange Request Payload',
    'description': 'Expected payload for an authentication code exchange request',
    'type': 'object',
    'properties': {
        'client_id': { 'type': 'string', 'minLength': 1 },
        'client_secret': { 'type': 'string', 'minLength': 1 },
        'state': { 'type': 'string', 'minLength': 1 },
        'code': { 'type': 'string', 'minLength': 1 },
        'grant_type': {'type': 'string', 'pattern': '^authentication_code$'},
        'response_type': {'type': 'string', 'pattern': '^tokens$'},
        'scope': { 'type': 'string', 'minLength': 1 },
    },
    'required': [
        'client_id',
        'client_secret',
        'state',
        'code',
        'grant_type',
        'response_type',
        'scope',
        ],
}
