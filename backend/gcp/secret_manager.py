from gcp.helpers import get_service_account_credentials
from google.cloud import secretmanager_v1


class SercretManager:
    def __init__(self):
        self.credentials = get_service_account_credentials()

    def get_secret_value(self, project, sercret, verion):
        name = f'projects/{project}/secrets/{sercret}/versions/{verion}'
        client = secretmanager_v1.SecretManagerServiceClient(credentials=self.credentials)
        response = client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8')
