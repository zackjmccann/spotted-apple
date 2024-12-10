from flask import Blueprint, request
from services.user import find_user, create_user, delete_user

user = Blueprint('user', __name__)

@user.route('/find', methods=['GET'])
def find():
    try:
        query_parameters = request.args
        id = int(query_parameters.get('id', None))
    except TypeError:
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Bad request: could not process user id',
            }
        }
    
    user = find_user(id=id)

    if user is None:
        return {
            'code': 404,
            'data': {
                'status': 'Error',
                'message': 'User not found',
            }
        }

    return {
        'code': 201,
        'data': {
            'status': 'success',
            'message': 'user found',
            'user': user.info
        }
    }


@user.route('/create', methods=['POST'])
def create():
    """
    Request must contain the following fields:
        - email
        - first_name
        - last_name
    """
    query_parameters = request.args
    user_data = {
        'email': query_parameters.get('email', None),
        'first_name': query_parameters.get('first_name', None),
        'last_name': query_parameters.get('last_name', None),
        }

    user = create_user(user_data)

    if user is None:
        return {
            'code': 400,
            'data': {
                'status': 'Error',
                'message': 'Failed to create user: Please ensure email, first name, and last name are not none.',
            }
        }

    return {
        'code': 201,
        'data': {
            'status': 'success',
            'message': 'New user created',
            'user': user.info
        }
    }

@user.route('/delete', methods=['POST'])
def delete():
    try:
        query_parameters = request.args
        id = int(query_parameters.get('id', None))
    except TypeError:
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Bad request: could not process user id',
            }
        }
    
    deleted_user = delete_user(id=id)

    if deleted_user is None:
        return {
            'code': 400,
            'data': {
                'status': 'Error',
                'message': 'Failed to delete user',
            }
        }

    return {
        'code': 201,
        'data': {
            'status': 'Success',
            'message': 'deleted user',
            'deleted_user': deleted_user,
        }
    }