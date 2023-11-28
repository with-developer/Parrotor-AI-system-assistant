from bson.objectid import ObjectId
from flask import Blueprint, render_template, request, Response, jsonify, stream_with_context, g
from ..db_utils import mongodb_connect
from ...API.account.account_verification_api import check_verification
from datetime import datetime, timedelta

db = mongodb_connect()

logs_dashboard_api_blueprint = Blueprint('logs_dashboard_api', __name__, url_prefix='/API/logs_dashboard')

# This Route: /API/logs_dashboard
@logs_dashboard_api_blueprint.route('/get', methods=['POST'])
@check_verification(['user','admin'])
def logs():
    page = int(request.form.get('page', 1))
    items_per_page = 5
    skip = (page - 1) * items_per_page
    
    total_logs = db.log.count_documents({})
    total_pages = -(-total_logs // items_per_page)  # 올림 나눗셈

    logs = {log['_id']: log for log in db.log.find({'log_type':'Linux Command Assistant'}).skip(skip).limit(items_per_page)}

    filtered_logs = {}
    for key, value in logs.items():
        filtered_logs[str(key)] = {
            'log_type' : value['log_type'],
            'user_id' : value['user_id'],
            'question' : value['question'],
            'answer' : value['answer'],
            'time' : value['time']
        }

    # return jsonify({"status" : "success", "message" : filtered_logs}), 200
    return jsonify({"status" : "success", "message": "로그 정보 조회 성공", "logs": filtered_logs, "total_pages": total_pages, "total_users": total_logs}), 201



@logs_dashboard_api_blueprint.route('/chart', methods=['GET'])
@check_verification(['user','admin'])
def chart():
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    pipeline = [
        {"$match": {"time": {"$gte": start_date.strftime('%Y-%m-%d'), "$lt": end_date.strftime('%Y-%m-%d')}}},
        {"$group": {"_id": {"$substr": ["$time", 0, 10]}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    logs_by_date = list(db.log.aggregate(pipeline))
    

    
    return jsonify({"status" : "success", "message": logs_by_date }), 201
