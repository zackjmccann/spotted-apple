from flask import Blueprint, request
from services.register import register_account, check_if_acccount_is_registered
from services.auth import issue_token


register = Blueprint('register', __name__)

@register.route('/account', methods=["POST"])
def account():
    try:
        data = request.get_json()
        account = register_account(data)

        if account.get('id', -1) != -1:
            access_token = issue_token(account.get('email'), account.get('id'), 10)
            refresh_token = issue_token(account.get('email'), account.get('id'), 10080) # 7 days

            return {
                'code': 201,
                'data': {
                    'status': 'Account Created',
                    'user_access_token': access_token,
                    'user_refresh_token': refresh_token,
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

@register.route('/introspect', methods=["POST"])
def introspect():
    try:
        data = request.get_json()
        is_registered = check_if_acccount_is_registered(data)
        return {
            'code': 200,
            'data': {
                'status': 'Success',
                'registered': is_registered,
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
