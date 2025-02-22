schema = {
    'title' : 'Token Introspection Request',
    'description': 'Expected payload token introspection request',
    'type': 'object',
    'properties': {
        'token': { 'type': 'string', 'minLength': 1 },
    },
    'required': ['token'],
}

type_mappings = {
    'token': 'str',
}