credentials_payload_schema = {
    'title' : 'Client Credential Authentication Request',
    'description': 'Expected payload for an authentication request to issue a token',
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 1
            },
        'password': {
            'type': 'string',
            'minLength': 1
            },
        'id': {
            'type': 'integer',
            },
        'grant_type': {
            'type': 'string',
            'pattern': '^client_credentials$'
            },
    },
    'required': ['username', 'password', 'id', 'grant_type'],
}
