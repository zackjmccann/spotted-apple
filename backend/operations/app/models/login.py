login_payload_schema = {
    'title' : 'Credential Based Login Authentication Request',
    'description': 'Expected payload for an login request',
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string',
            'minLength': 1
            },
        'password': {
            'type': 'string',
            'minLength': 1
            },
        'grant_type': {
            'type': 'string',
            'pattern': '^authorization$'
            },
    },
    'required': ['email', 'password', 'grant_type'],
}
