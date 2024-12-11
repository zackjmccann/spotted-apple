from database import aloe

def email_is_registered(email: str) -> bool:
    """
    Query the Aloe for the prodivde email

    Params:
        email: str
            The email to check Aloe for
    Return:
        bool
            Whether the email is found in Aloe
    """
    query_response = aloe.get_user_email(email=email)

    try:
        assert query_response.get('email', None) == email and email is not None
        return True
    except AssertionError:
        return False
