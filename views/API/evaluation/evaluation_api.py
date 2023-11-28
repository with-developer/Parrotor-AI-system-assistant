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
def evaluation():
    

    page = int(request.form.get('page', 1))
    items_per_page = 10
    skip = (page - 1) * items_per_page
    
    total_data = db.account.count_documents({"approved": {"$ne": False}})
    total_pages = -(-total_data // items_per_page)  # 올림 나눗셈

    print(total_data)
    data = {data['_id']: data for data in db.account.find({"approved": {"$ne": False}}).skip(skip).limit(items_per_page)}
    print(data)
    top_commands_and_questions_by_user = {}
    for user_id, user_data in data.items():
        user_id_value = user_data['user_id']  # 사용자의 user_id 추출
        command_level = user_data['command_level']
        try:
            security_level = round(user_data['security_level']['correct']/(user_data['security_level']['correct'] + user_data['security_level']['incorrect']),2)*100
        except ZeroDivisionError as e:
            security_level = 0

        # 명령어와 사용 횟수를 사용 횟수에 따라 내림차순으로 정렬
        sorted_commands = sorted(command_level.items(), key=lambda x: x[1], reverse=True)[:5]
        # 상위 5개 명령어 이름만 추출하여 집합으로 저장
        top_command_names = [command[0] for command in sorted_commands]

        # db.logs에서 해당 user_id의 질문 개수 계산
        question_count = db.log.count_documents({"user_id": user_id_value})

        # 결과 사전에 추가
        top_commands_and_questions_by_user[user_id_value] = {
            'commands': top_command_names,
            'question_count': question_count,
            'security_level': security_level
        }


    print()
    print(top_commands_and_questions_by_user)
    # filtered_logs = {}
    # for key, value in logs.items():
    #     print("key:",key)
    #     print("value:",value)
    #     print()

        
    #     filtered_logs[str(key)] = {
    #         'log_type' : value['log_type'],
    #         'user_id' : value['user_id'],
    #         'question' : value['question'],
    #         'answer' : value['answer'],
    #         'time' : value['time']
    #     }

    # print("logs:",filtered_logs)


        
    # return jsonify({"status" : "success", "message" : filtered_logs}), 200
    return jsonify({"status" : "success", "message": "로그 정보 조회 성공", "data": top_commands_and_questions_by_user, "total_pages": total_pages, "total_users": total_data}), 201
