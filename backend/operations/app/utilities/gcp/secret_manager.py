from gcp.helpers import get_service_account_credentials
from google.cloud import secretmanager_v1
from google.api_core import exceptions


class SercretManager:
    def __init__(self):
        self.credentials = get_service_account_credentials()
        self.client = self._get_client()

    def create_secret(self, parent: str, secret_id: str):
        return self.client.create_secret(
            secret_id=secret_id,
            parent=f"projects/{parent}",
            secret={'replication': {'automatic': {}}})

    def add_secret_version(self, project: str, secret_id: str, data: str):
        parent = f"projects/{project}/secrets/{secret_id}"
        payload = data.encode('UTF-8')
        return self.client.add_secret_version(
            parent=parent,
            payload={'data': payload}
            )

    def get_secret_value(self, secret: str):
        try:
            response = self.client.access_secret_version(name=secret)
            return response.payload.data.decode('UTF-8')
        except exceptions.FailedPrecondition:
            print('Secret is disabled')

    def list_secrets(self, parent: str):
        request = secretmanager_v1.ListSecretsRequest(parent=parent)
        return self.client.list_secrets(request=request)

    def list_secret_versions(self, parent: str):
        request = secretmanager_v1.ListSecretVersionsRequest(parent=parent)
        return self.client.list_secret_versions(request=request)

    def get_secret(self, name: str):
        request  = secretmanager_v1.GetSecretRequest(name=name)
        return self.client.get_secret(request=request)

    def parse_secret_version_path(self, secret):
        return self.client.parse_secret_version_path(secret)
   
    def _get_client(self):
        return secretmanager_v1.SecretManagerServiceClient(credentials=self.credentials)
