client_credentials_payload_schema = {
    'title' : 'Client Credential Authentication Request',
    'description': 'Expected payload for an authentication request to issue a token',
    'type': 'object',
    'properties': {
        'client_id': {
            'type': 'string',
            'minLength': 1
            },
        'username': {
            'type': 'string',
            'minLength': 1
            },
        'secret': {
            'type': 'string',
            'minLength': 1
            },
        'grant_type': {
            'type': 'string',
            'pattern': '^client_credentials$'
            },
    },
    'required': ['client_id', 'username', 'secret', 'grant_type'],
}
