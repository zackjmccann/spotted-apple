schema = {
    'title' : 'Credential Based Login Authentication Request',
    'description': 'Expected payload for a login request',
    'type': 'object',
    'properties': {
        'grant_type': { 'type': 'string', 'pattern': '^authorization$' },
        'email': { 'type': 'string', 'minLength': 1 },
        'password': { 'type': 'string', 'minLength': 1 },
    },
    'required': ['grant_type', 'email', 'password'],
}

type_mappings = {
    'grant_type': 'str',
    'email': 'str',
    'password': 'str',
}