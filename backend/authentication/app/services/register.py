import os
import bcrypt
from database import aloe
from auth_logging import logger
from models.register import account_payload_schema, registered_check_payload_schema
from utilities.payload_handlers import sanitize
from jsonschema import ValidationError


SECRET_KEY = os.getenv('SECRET_KEY')
ALOGRITHMS = os.getenv('JWT_ALORITHM')
APP_ID = os.getenv('APP_ID')
GRANTED_APP_IDS = os.getenv('GRANTED_APP_IDS')

def register_account(payload):
    try:
        playload_mapping = {'email': 'str', 'password': 'str'}
        clean_payload = sanitize(payload, account_payload_schema, playload_mapping)
        clean_email, clean_password = clean_payload.values()
        password_hash, password_salt = _hash_password(clean_password)
        new_account = aloe.register_account(clean_email, password_hash, password_salt)
        print(new_account)

        return new_account

    except (ValidationError, ValueError, KeyError):
        return {
            'code': 400,
            'data': {
                'notice': 'Registration was unsuccessful',
                'account': {'id': -1}
                },
            }

def check_if_acccount_is_registered(payload):
    try:
        playload_mapping = {'email': 'str'}
        clean_payload = sanitize(payload, registered_check_payload_schema, playload_mapping)
        clean_email = clean_payload.get('email', None)
        result = aloe.get_user_email(clean_email)

        if result is None:
            is_registered = False
        else:
            assert result.get('email', None) == clean_email
            is_registered = True

        return is_registered

    except (ValidationError, ValueError, KeyError, AssertionError):
        return {
            'code': 400,
            'data': {
                'registered': None,
                'message': 'Registration check was unsuccessful',
                },
            }

def _hash_password(password):
    hash_bytes = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(hash_bytes, salt).hex()
    return hash, str(salt)
