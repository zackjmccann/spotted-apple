import os
import bcrypt
from jsonschema import validate, ValidationError
from database import aloe
from auth_logging import logger
from models.register import account_payload_schema


SECRET_KEY = os.getenv('SECRET_KEY')
ALOGRITHMS = os.getenv('JWT_ALORITHM')
APP_ID = os.getenv('APP_ID')
GRANTED_APP_IDS = os.getenv('GRANTED_APP_IDS')

def register_account(payload):
    try:
        clean_email, clean_password = _sanitize(payload)
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

def _sanitize(payload):
    validate(instance=payload, schema=account_payload_schema)
    _check_for_dangerous_characters(payload)
    email = str(payload['email'])
    password = str(payload['password'])
    return email, password

def _check_for_dangerous_characters(payload):
    forbidden_characters = ['$', '..', ';', '--']
    for field in ['email', 'password']:
        for character in forbidden_characters:
            if character in payload[field]:
                raise ValueError('Payload contains forbidden character')

def _hash_password(password):
    hash_bytes = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(hash_bytes, salt).hex()
    return hash, str(salt)
