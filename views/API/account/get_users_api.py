from flask import Blueprint, request, jsonify
from ..db_utils import mongodb_connect
from ...API.account.account_verification_api import check_verification

get_users_api_blueprint = Blueprint('get_users_api', __name__, url_prefix='/API/account')

db = mongodb_connect()

# get_users_api route: /API/account/get-users
@get_users_api_blueprint.route('/get-users', methods=['POST'])
@check_verification(['admin'])
def get_users_api():
    users = {user['_id']: user for user in db.account.find()}
    filtered_users = {}
    for user_id, user_info in users.items():
        filtered_users[str(user_id)] = {
            'user_name': user_info['user_name'],
            'user_id': user_info['user_id'],
            'user_pw': user_info['user_pw'],
            'fail_count': user_info['fail_count'],
            'approved': user_info['approved']
        }
    print("users:",filtered_users)

    return jsonify({"status" : "success", "message": "계정 정보 조회 성공", "users": filtered_users}), 201