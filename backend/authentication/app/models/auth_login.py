schema = {
    'title' : 'Credential Based Login Authentication Request',
    'description': 'Expected payload for a login request',
    'type': 'object',
    'properties': {
        'client_id': { 'type': 'string', 'minLength': 1 },
        'client_name': { 'type': 'string', 'minLength': 1 },
        'client_secret': { 'type': 'string', 'minLength': 1 },
        'grant_type': { 'type': 'string', 'pattern': '^authorization$' },
        'email': { 'type': 'string', 'minLength': 1 },
        'password': { 'type': 'string', 'minLength': 1 },
    },
    'required': ['client_id', 'client_name', 'client_secret', 'grant_type', 'email', 'password'],
}

type_mappings = {
    'client_id': 'str',
    'client_name': 'str',
    'client_secret': 'str',
    'grant_type': 'str',
    'email': 'str',
    'password': 'str',
}