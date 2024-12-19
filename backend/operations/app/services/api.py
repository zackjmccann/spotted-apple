from services.auth import call_auth_server, AuthenticationError


def email_is_registered(email: str, headers: dict) -> bool:
    """
    Call Auth service to validate if an email is already registered

    Params:
        email: str
            The email to check
    Return:
        bool
            Whether the email is registered
    """
    try:
        response = call_auth_server(
            '/register/introspect',
            {'email': email},
            {
                'Content-Type': headers.get('Content-Type'),
                'Authorization': headers.get('Authorization'),
            }) 
   
        if response.status_code == 200:
            data = response.json()
            return data['registered']
        else:
            err_data = response.json()
            err =  AuthenticationError(err_data['message'])
            err.code = response.status_code
            err.status = err_data['status']
            raise err

    except AssertionError:
        return False
