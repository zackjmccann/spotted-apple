from flask import Blueprint, request, make_response
from services.register import register_account

register = Blueprint('register', __name__)

@register.route('/account', methods=["POST"])
def account():
    try:
        data = request.get_json()
        account = register_account(data)

        if account.get('id', -1) != -1:
            return {
                'code': 201,
                'data': {
                    'account': account
                    },
                }
        else:
            return {
                'code': 400,
                'data': {
                    'status': 'Failed',
                    'notice': 'Registration was unsuccessful',
                    },
                }

    except (TypeError, KeyError):
        return {
            'code': 400,
            'data': {
                'status': 'Failed',
                'message': 'Account registration failed',
            }
        }
