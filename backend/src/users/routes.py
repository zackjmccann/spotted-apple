import requests
from flask import Blueprint, request, jsonify
from database.aloe import Aloe
from users.models import User

users_blueprint = Blueprint('users', __name__)
aloe = Aloe()

@users_blueprint.route('/get', methods=['GET'])
def get_user():
    try:
        query_parameters = request.args
        id = int(query_parameters.get('id', None))
    except TypeError:
        return jsonify({
            'status': 'error',
            'message': 'Bad request: could not process user id'
        }), 400
    
    query_response = aloe.get_user(id=id)
    if not query_response:
        return jsonify({
            'status': 'error',
            'message': 'No user found with provided id'
        }), 404

    user = User(query_response)

    return jsonify({
        'status': 'success',
        'message': 'user found',
        'user': user.info
        }), 201

@users_blueprint.route('/create', methods=['POST'])
def create_user():
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

    user = User(user_data)
    if not user.is_valid:
        return jsonify({
            'status': 'error',
            'message': 'Bad request: could not create new user'
        }), 400
    
    query_response = aloe.insert_user(user_data=user.info)
    user.add_fields(query_response)

    return jsonify({
        'status': 'success',
        'message': 'new user created',
        'user': user.info
        }), 201

@users_blueprint.route('/delete', methods=['POST'])
def delete_user():
    try:
        query_parameters = request.args
        id = int(query_parameters.get('id', None))
    except TypeError:
        return jsonify({
            'status': 'error',
            'message': 'Bad request: could not process user id'
        }), 400
    
    query_response = aloe.delete_user(id=id)
    deleted_id = query_response.get('id', -1)

    return jsonify({
        'status': 'success',
        'message': 'deleted user',
        'user': deleted_id
        }), 201
