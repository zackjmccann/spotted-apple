schema = {
    'title' : 'Token Refresh Request',
    'description': 'Expected payload token refresh request',
    'type': 'object',
    'properties': {
        'token': { 'type': 'string', 'minLength': 1 },
    },
    'required': ['token'],
}

type_mappings = {
    'token': 'str',
}