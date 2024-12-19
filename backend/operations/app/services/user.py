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

def create_user(user_data: dict) -> User:
    user = User(user_data)

    if not user.is_valid:
        user = None
    
    query_response = aloe.insert_user(user_data=user.info)
    user.add_fields(query_response)

    return user

def delete_user(id: int) -> int:
    query_response = aloe.delete_user(user_data=id)
    if query_response is None:
        return None
    return query_response['id']
