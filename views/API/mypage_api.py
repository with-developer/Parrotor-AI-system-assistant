from flask import Blueprint, render_template, request, jsonify, g
from .db_utils import mongodb_connect
from dotenv import load_dotenv
from flask_mail import Mail, Message
from ..API.account.account_verification_api import check_verification
import os

mypage_api_blueprint = Blueprint('mypage_api',__name__, url_prefix='/API/mypage')

db = mongodb_connect

load_dotenv(verbose=True)
SECRET_KEY = os.getenv('SECRET_KEY')

# This is Route: /API/mypage
@mypage_api_blueprint.route('/', methods=['POST'])
@check_verification(['user','admin'])
# 1. ID, Name, Auth 출력   
# 2. pw 변경   
# 3. 로그 출력 

def mypage_info_api():
    user_id = g.user_id
    user_name = g.user_name
    user_role = g.user_role
    return jsonify({'user_id': user_id, 'user_name': user_name, 'user_auth': user_role})


def mypage_change_pw_api():
    # FE에서 전송된 회원가입 정보를 get_json 함수로 받아옴
    user_data = request.get_json()

    # get_json을 통해 받아온 데이터의 각 정보들을 따로 추출
    user_id = user_data.get('user_id')
    user_name = user_data.get('user_name')

    # user_name으로 해당 사용자의 user_info를 검색
    user_id_info = db.account.find_one({'user_id': user_id})
    user_name_info = db.account.find_one({'user_name': user_name})

    # 사용자가 존재하지 않는 경우 
    if not user_id_info:
        return jsonify({"status" : "fail", "message": "존재하지 않는 ID입니다."}), 400

    # 메일 보내기
    from app import app
    mail = Mail(app)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    # TODO: MAIL_USERNAME, MAIL_PASSWORD는 환경 변수에 저장
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    recipients = ['user_email_info']
    # TODO: sender, recipients 입력
    msg = Message('jirangobie: 비밀번호 변경을 위한 메일입니다.', sender = '', recipients=[''])

    user_name_pwchange = user_id_info.get('name', '')
    msg.body = user_name_pwchange+'님의 비밀번호 변경 요청이 들어왔습니다. 비밀번호를 변경해주시기 바랍니다. '
    mail.send(msg)


    # 3. 로그 출력
    
    