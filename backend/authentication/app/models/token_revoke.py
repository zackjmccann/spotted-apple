schema = {
    'title' : 'Token Revoke Request',
    'description': 'Expected payload token revoke request',
    'type': 'object',
    'properties': {
        'token': { 'type': 'string', 'minLength': 1 },
    },
    'required': ['token'],
}

type_mappings = {
    'token': 'str',
}