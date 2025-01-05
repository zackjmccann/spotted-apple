"""
A class for managing client sessions
"""
from database import aloe
from models import session_schema
from jsonschema import ValidationError
from utilities.payload_handlers import validate_with_datetime
from app.services import BaseService


class SessionError(Exception):
    pass


class SessionService(BaseService):
    def __init__(self):
        super().__init__()
        self.db_conn = aloe
    
    def create_session(self, client_id: str) -> dict:
        """
        Create a session for a client

        Client IDs are used to create a session in Aloe,
        and session consist of the associated client ID,
        a session ID, and a session state.
        """
        try:
            assert type(client_id) == str
            session = self.db_conn.create_session(client_id)
            validate_with_datetime(
                instance=session,
                schema=session_schema)
            return session
        except (AssertionError, ValidationError):
            raise SessionError('Failed to create session')

    
    def revoke_session(self, session_id: str) -> dict:
        """Revoke a session for a client"""
        try:
            assert type(session_id) == str
            if self.validate_session(session_id):
                revoked = self.db_conn.revoke_session(session_id)
                assert revoked
                return revoked
            else:
                return True
        except AssertionError:
            raise SessionError('Failed to revoke session')

    def validate_session(self, session_id: str):
        """
        Validate a session based on id

        Sessions are valid if a record exists in the database
        with the session id, and the expiration has not surpassed at
        the time of validation.
        """
        try:
            assert type(session_id) == str
            response = self.db_conn.validate_session(session_id)
            is_valid = response['valid']
            return is_valid
        except AssertionError:
            raise SessionError('Failed to validate session')

    def get_session_state(self, session_id: str):
        """Get the session_state value associated with a session"""
        try:
            assert type(session_id) == str
            response = self.db_conn.get_session_state(session_id)
            session_state = response.get('session_state', None)
            if not session_state:
                raise SessionError('Failed to get session state')
            return session_state
        except AssertionError:
                raise SessionError('Failed to get session state')
