schema = {
    'title' : 'Service Authentication Request',
    'description': 'Expected payload for an authentication request from a registered service',
    'type': 'object',
    'properties': {
        'service_id': {
            'type': 'string',
            'minLength': 1
            },
        'service_name': {
            'type': 'string',
            'minLength': 1
            },
        'service_secret': {
            'type': 'string',
            'minLength': 1
            },
        'grant_type': {
            'type': 'string',
            'pattern': '^client_credentials$'
            },
    },
    'required': ['service_id', 'service_name', 'service_secret', 'grant_type'],
}

type_mappings = {
    'service_id': 'str',
    'service_name': 'str',
    'service_secret': 'str',
    'grant_type': 'str',
}
