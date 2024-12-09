from flask import Blueprint

test_bp = Blueprint('test', __name__)

@test_bp.route('/foo', methods=['GET'])
def foo():

    response = {
        'code': 201,
        'data': {
            'message': 'bar',
            'data': {'foo': 'bar'},
            'things': [1,2,3],
        }
    }

    return response