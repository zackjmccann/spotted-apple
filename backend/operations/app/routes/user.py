from flask import Blueprint, request
from services.user import find_user

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
