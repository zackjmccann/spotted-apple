url_parameters_schema = {
    'title' : 'URL Parameters for authentication and authorization requests',
    'description': 'Expected URL parameters for authentication requests',
    'type': 'object',
    'properties': {
        'client_id': { 
            'type': 'string',
            'minLength': 1
            },
        'redirect_uri': {
            'type': 'string',
            'minLength': 1
            },
        'state': {
            'type': 'string',
            'minLength': 1
            },
        'response_type': {
            'type': 'string',
            'pattern': '^code$'
            },
        'scope': {
            'type': 'string',
            'minLength': 1
            },
        'code_challenge': {
            'type': 'string',
            'minLength': 1
            },
        'code_challenge_method': {
            'type': 'string',
            'pattern': '^S256$'
            },
    },
    'required': [
        'client_id',
        'redirect_uri',
        'state',
        'response_type',
        'scope',
        'code_challenge',
        'code_challenge_method',
        ],
}

