from flask import Blueprint, request, jsonify
from ..db_utils import mongodb_connect
from ...API.account.account_verification_api import check_verification

get_users_api_blueprint = Blueprint('get_users_api', __name__, url_prefix='/API/account')

db = mongodb_connect()

# get_users_api route: /API/account/get-users
@get_users_api_blueprint.route('/get-users', methods=['POST'])
@check_verification(['admin'])
def get_users_api():
    page = int(request.form.get('page', 1))
    items_per_page = 10
    skip = (page - 1) * items_per_page
    
    total_users = db.account.count_documents({})
    total_pages = -(-total_users // items_per_page)  # 올림 나눗셈

    users = {user['_id']: user for user in db.account.find().skip(skip).limit(items_per_page)}
    filtered_users = {}
    for user_id, user_info in users.items():
        filtered_users[str(user_id)] = {
            'user_name': user_info['user_name'],
            'user_id': user_info['user_id'],
            'role': user_info['role'],
            'fail_count': user_info['fail_count'],
            'approved': user_info['approved'],
            'lastlogin' : user_info['lastlogin']
        }
    print("users:",filtered_users)

    return jsonify({"status" : "success", "message": "계정 정보 조회 성공", "users": filtered_users, "total_pages": total_pages, "total_users": total_users}), 201