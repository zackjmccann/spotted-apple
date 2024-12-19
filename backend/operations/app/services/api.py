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
                'Content-Type': headers.get('Content-Type'), # 'application/json'
                'Authorization': headers.get('Authorization'), # 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzcG90dGVkLWFwcGxlLWJhY2tlbmQiLCJhdWQiOlsiMSJdLCJpYXQiOjE3MzQ1MDExODksImV4cCI6MTczNDUwMTc4OSwianRpIjoiYmFja2VuZF9zZXJ2aWNlc18yMDI0MTIxOF8wMDUzIiwiY29udGV4dCI6eyJ1c2VybmFtZSI6ImZyb250ZW5kIiwicm9sZXMiOlsiY2xpZW50Il19fQ.4iLJgRy2bSEbVCyTogs5kF3rwzcyJpXVFtKQqszf5cY'
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
