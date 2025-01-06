import jwt
import datetime
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
              be concatinated with the ops server ID and used as the JTI
        """
        try:
            assert self._validate_audience(aud)
            jti = f'{self.id}-{context["id"]}'
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

    def issue_service_tokens(self, service_data: str) -> str:
        """Create access and refresh JWTs for a service"""
        name = service_data.get('service_name')
        iat = datetime.datetime.now(datetime.timezone.utc)
        context = {
            'id': service_data.get('id'),
            'roles':['service'],
        }
        
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
                token: self.issue_token(name, iat, config['exp'], context)})
        
        return tokens

    def validate_token(self, token: str):
        try:
            token_data = self.decode_token(token)
            assert token_data
            return True
        except (AssertionError, TokenError):
            return False

    def _validate_audience(self, aud: str) -> bool:
        """
        Validate that the provided aud value for a token is know, and granted
        the abilities to be issued tokens
        """
        return aud in self.granted_aud
