account_payload_schema = {
    'title' : 'Registration Account Request',
    'description': 'Expected payload for a request to the register/account endpoint',
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

registered_check_payload_schema = {
    'title' : 'Registration Account Check Request',
    'description': 'Expected payload for a request to check if an email is registered',
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string',
            'format': 'email'
            },
    },
    'required': ['email'],
}