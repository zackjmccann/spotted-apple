import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALOGRITHMS = os.getenv('JWT_ALORITHM')
APP_ID = os.getenv('APP_ID')
GRANTED_APP_IDS = os.getenv('GRANTED_APP_IDS')


# if None in [SECRET_KEY, ALOGRITHMS, APP_ID]:
#     raise AuthenticationError('An authentication failure occurred')

def validate_token(token):
    # TODO: Refactor route to call to the auth endpoint
    pass