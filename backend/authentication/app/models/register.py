account_payload_schema = {
    'title' : 'Registration Account Request',
    'description': 'Expected payload for a request to the registar/account endpoint',
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string',
            'format': 'email'
            },
        'password': {
            'type': 'string',
            'minLength': 1
            },
    },
    'required': ['email', 'password'],
}
