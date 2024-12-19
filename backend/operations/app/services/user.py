from database import aloe
from models.user import User

def find_user(id: int) -> User:
    """
    Query the Aloe for the prodivde user id

    Params:
        email: str
            The email to check Aloe for
    Return:
        User
            Model of user
    """
    query_response = aloe.get_user(id=id)
    if query_response is None:
        return None

    return User(query_response)
