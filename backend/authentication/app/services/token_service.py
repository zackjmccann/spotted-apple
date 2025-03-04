import jwt
import datetime
from database import AloeError
from app.services.base_service import BaseService
from app.services.errors import TokenError


class TokenService(BaseService):
    def __init__(self, app):
        super().__init__(app)
        self.id = self._get_environment_variable('ID')
        self.secret_key = self._get_environment_variable('SECRET_KEY')
        self.alogrithms = self._get_environment_variable('JWT_ALORITHM')
        self.granted_aud = self._get_environment_variable('GRANTED_AUD', 'list')

    def issue_token(self, aud: str, iat: datetime, exp: datetime, context: dict) -> str:
        """
        Create a JWT

        Note: It is expected the context has an "id" field, which will
              be concatenated with the application ID and used as the JTI
        """
        try:
            assert self._validate_audience(aud)
            jti = f'{self.id}-{context["id"]}-{str(iat.timestamp())}'
            data = {
                'iss': 'spotted-apple-auth-service',
                'aud': [aud],
                'iat': iat,
                'exp': exp,
                'jti': jti,
                'context': context,
            }

            return jwt.encode(data, self.secret_key, self.alogrithms)

        except AssertionError:
            raise TokenError(f'{aud} audience not granted access to tokens.')
        except KeyError:
            raise TokenError(f'ID not provided for token creation.')

    def decode_token(self, token: str):
        """Decode a JWT"""
        if not token:
            raise TokenError('Invalid Token')
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.alogrithms],
                audience=self.granted_aud)
        except jwt.ExpiredSignatureError:
            raise TokenError('Token Expired')
        except jwt.InvalidTokenError:
            raise TokenError('Token Invalid')

    def issue_user_access_tokens(self, user_data: str) -> str:
        """
        Create access and refresh JWTs for a user
        
        Tokens issued to users are associated with a registered client. The client ID
        and name leveraged for audience fields, and the user email is stored within
        the token context.
        """
        try:
            client_id = user_data['client_id']
            client_name = user_data['client_name']
            email = user_data['email']
        except KeyError:
            raise TokenError('User data invalid')

        iat = datetime.datetime.now(datetime.timezone.utc)
        context = { 'id': client_id, 'roles':['user'], 'user': email}

        token_configs = {
            'access': {
                'exp': iat + datetime.timedelta(minutes=5),
                },
            'refresh': {
                'exp': iat + datetime.timedelta(minutes=60 * 24 * 7),
                },
        }

        tokens = {}
        for token, config in token_configs.items():
            tokens.update({
                token: self.issue_token(client_name, iat, config['exp'], context)})

        return tokens

    def validate_token(self, token: str):
        try:
            response = self.app.db.check_token_blacklist(token)
            self.app.logger.debug(f'Response: {response["token_is_blacklisted"]}')
            assert not response['token_is_blacklisted'] or response['token_is_blacklisted'] is None
            token_data = self.decode_token(token)
            assert token_data
            return True
        except(AssertionError, TokenError):
            return False

    def revoke_token(self, token: str):
        """Add a token to the blacklist in Aloe"""
        try:
            response = self.app.db.blacklist_token(token)
            assert response['token'] == token
            return True

        except AloeError:
            self.app.logger.warning('Token already in blacklist.')
            return True

        except AssertionError:
            self.app.logger.critical('Failed to blacklist token')
            return False

    def refresh_access(self, token: str) -> dict:
        valid_token = self.validate_token(token)
        if not valid_token:
            raise TokenError('Invalid refresh token.')

        token_data = self.decode_token(token)
        context = token_data.get('context')

        user_access_data = {
            'client_id': context.get('id'),
            'client_name': token_data.get('aud')[0],
            'email': context.get('user'),
        }

        tokens = self.issue_user_access_tokens(user_access_data)
        self.revoke_token(token)
        return tokens

    def _validate_audience(self, aud: str) -> bool:
        """
        Validate that the provided aud value for a token is known and granted
        the abilities to be issued tokens
        """
        return aud in self.granted_aud
