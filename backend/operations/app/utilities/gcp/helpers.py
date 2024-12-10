import os
from distutils.util import strtobool
from google.oauth2 import service_account

def get_service_account_credentials():
    """
    Retrieve the service account credentials found via
    the GOOGLE_SERVICE_ACCOUNT environment variable.
    """
    dev_mode = bool(strtobool(os.getenv('DEV_MODE', 'False')))

    if dev_mode:
        credentials = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
        return service_account.Credentials.from_service_account_file(credentials)
    
    credentials = os.getenv('GOOGLE_SERVICE_ACCOUNT')
    return service_account.Credentials.from_service_account_info(credentials)
