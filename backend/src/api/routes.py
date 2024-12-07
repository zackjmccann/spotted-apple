from flask import Blueprint, request, jsonify
from database.aloe import Aloe


api_blueprint = Blueprint('api', __name__)
aloe = Aloe()

@api_blueprint.route('/check-email', methods=['POST'])
def check_email():
    try:
        query_parameters = request.args
        email = query_parameters.get('email')
    except KeyError:
        return jsonify({
            'status': 'error',
            'message': 'Bad request: did not contain an email'
        }), 400
    
    query_response = aloe.get_user_email(email=email)
    if not query_response:
        return jsonify({'status': 'success', 'exists': False}), 200
    
    try:
        assert query_response.get('email') == email
        return jsonify({'status': 'success', 'exists': True}), 200

    except AssertionError:
        return jsonify({
            'status': 'error',
            'message': 'Cannot process email check'
        }), 404

