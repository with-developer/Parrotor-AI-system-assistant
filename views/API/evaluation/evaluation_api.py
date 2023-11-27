from bson.objectid import ObjectId
from flask import Blueprint, render_template, request, Response, jsonify, stream_with_context, g
from ..db_utils import mongodb_connect
from ...API.account.account_verification_api import check_verification
from dotenv import load_dotenv



db = mongodb_connect()

evaluation_api_blueprint = Blueprint('evaluation_api', __name__, url_prefix='/API/evaluation')

# This Route: /API/evaluation
@evaluation_api_blueprint.route('/get', methods=['POST'])
@check_verification(['user','admin'])
def logs():
    

    page = int(request.form.get('page', 1))
    items_per_page = 6
    skip = (page - 1) * items_per_page
    
    total_logs = db.log.count_documents({})
    total_pages = -(-total_logs // items_per_page)  # 올림 나눗셈

    logs = {log['_id']: log for log in db.log.find({'log_type':'Linux Command Assistant'}).skip(skip).limit(items_per_page)}
    print(logs)
    filtered_logs = {}
    for key, value in logs.items():
        print("key:",key)
        print("value:",value)
        print()

        
        filtered_logs[str(key)] = {
            'log_type' : value['log_type'],
            'user_id' : value['user_id'],
            'question' : value['question'],
            'answer' : value['answer'],
            'time' : value['time']
        }

    print("logs:",filtered_logs)
    
        
    # return jsonify({"status" : "success", "message" : filtered_logs}), 200
    return jsonify({"status" : "success", "message": "로그 정보 조회 성공", "logs": filtered_logs, "total_pages": total_pages, "total_users": total_logs}), 201
