login_payload_schema = {
    'title' : 'Credential Based Login Authentication Request',
    'description': 'Expected payload for an login request',
    'type': 'object',
    'properties': {
        'client_id': { 'type': 'string', 'minLength': 1 },
        'client_secret': { 'type': 'string', 'minLength': 1 },
        'state': { 'type': 'string', 'minLength': 1 },
        'response_type': { 'type': 'string', 'pattern': '^code$' },
        'scope': { 'type': 'string', 'minLength': 1 },
        # 'code_challenge': { 'type': 'string', 'minLength': 1 },
        # 'code_challenge_method': { 'type': 'string', 'pattern': '^S256$' },
        'email': { 'type': 'string', 'minLength': 1 },
        'password': { 'type': 'string', 'minLength': 1 },
        'grant_type': { 'type': 'string', 'pattern': '^authorization$' },
    },
    'required': [
        'client_id',
        'client_secret',
        'state',
        'response_type',
        'scope',
        # 'code_challenge',
        # 'code_challenge_method',
        'email',
        'password',
        'grant_type',
        ],
}
