from flask import Blueprint, render_template, request, jsonify, g
from ..db_utils import mongodb_connect
from dotenv import load_dotenv
from ...API.account.account_verification_api import check_verification
import os

dash_userinfo_api_blueprint = Blueprint('dash_userinfo_api',__name__, url_prefix='/API/account')

db = mongodb_connect()

load_dotenv(verbose=True)
SECRET_KEY = os.getenv('SECRET_KEY')

# This is Route: /API/dash_userinfo
@dash_userinfo_api_blueprint.route('/dash_userinfo', methods=['POST'])
@check_verification(['user','admin'])
# 1. ID, Name, Auth 출력   
# 2. pw 변경   XX

def dash_userinfo_api():
    user_id = g.user_id
    user_name = g.user_name
    user_role = g.user_role
    user_data = db.account.find_one({'user_id': user_id})

    # security_level 필드에서 correct와 incorrect 값 추출
    if user_data and 'security_level' in user_data:
        correct = user_data['security_level'].get('correct', 0)
        incorrect = user_data['security_level'].get('incorrect', 0)
        print(f'Correct: {correct}, Incorrect: {incorrect}')
    else:
        print('User not found or security_level not available')
    
    try:
        user_evaluation = round(user_data['security_level']['correct']/(user_data['security_level']['correct'] + user_data['security_level']['incorrect']),2)*100
    except ZeroDivisionError as e:
        user_evaluation = 0

    question_count = db.log.count_documents({"user_id": user_id})
    return jsonify({'user_id': user_id, 'user_name': user_name, 'user_auth': user_role, 'user_evaluation' : user_evaluation, 'question_count' : question_count})


# def mypage_change_pw_api():
#     # FE에서 전송된 회원가입 정보를 get_json 함수로 받아옴
#     user_data = request.get_json()

#     # get_json을 통해 받아온 데이터의 각 정보들을 따로 추출
#     user_id = user_data.get('user_id')
#     user_name = user_data.get('user_name')

#     # user_name으로 해당 사용자의 user_info를 검색
#     user_id_info = db.account.find_one({'user_id': user_id})
#     user_name_info = db.account.find_one({'user_name': user_name})

#     # 사용자가 존재하지 않는 경우 
#     if not user_id_info:
#         return jsonify({"status" : "fail", "message": "존재하지 않는 ID입니다."}), 400

#     # 메일 보내기
#     from app import app
#     mail = Mail(app)

#     app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#     app.config['MAIL_PORT'] = 465
#     # TODO: MAIL_USERNAME, MAIL_PASSWORD는 환경 변수에 저장
#     app.config['MAIL_USERNAME'] = ''
#     app.config['MAIL_PASSWORD'] = ''
#     app.config['MAIL_USE_TLS'] = False
#     app.config['MAIL_USE_SSL'] = True
#     mail = Mail(app)
#     recipients = ['user_email_info']
#     # TODO: sender, recipients 입력
#     msg = Message('jirangobie: 비밀번호 변경을 위한 메일입니다.', sender = '', recipients=[''])

#     user_name_pwchange = user_id_info.get('name', '')
#     msg.body = user_name_pwchange+'님의 비밀번호 변경 요청이 들어왔습니다. 비밀번호를 변경해주시기 바랍니다. '
#     mail.send(msg)