schema = {
    'title' : 'Client Identification Information',
    'description': 'Expected format for client identification info',
    'type': 'object',
    'properties': {
        'client_id': {'type': 'string', 'minLength': 1},
        'client_name': {'type': 'string', 'minLength': 1},
        'client_secret': {'type': 'string', 'minLength': 1},
    },
    'required': ['client_id', 'client_name', 'client_secret'],
}

type_mappings = {
    'client_id': 'str',
    'client_name': 'str',
    'client_secret': 'str',
}
