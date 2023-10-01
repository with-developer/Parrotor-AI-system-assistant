from flask import Blueprint, render_template, request, jsonify
from ..db_utils import mongodb_connect
from .hash_password import hash_password
import jwt
import datetime
import os
from dotenv import load_dotenv

signin_api_blueprint = Blueprint('signin_api', __name__, url_prefix='/API/account')

db = mongodb_connect()

load_dotenv(verbose=True)
SECRET_KEY = os.getenv('SECRET_KEY')

# This Route: /API/account/signin
@signin_api_blueprint.route('/signin', methods=['POST'])
def signin_api():
    """ TODO
    1. DB에 userid가 존재하는지 체크
    2. userpw에 솔트값 추가 및 sha256 해싱 후 DB의 userid의 패스워드와 동일한지 체크
    주의사항 1: 패스워드가 틀렸을 경우 DB에 fail_count 1 증가
    주의사항 2: 패스워드가 맞으면 DB에 fail_count 0으로 초기화
    주의사항 3: DB에 fail_count가 5와 같거나 크다면 접속 불가
    3. JWT token 발급
    """
    # FE에서 전송된 회원가입 정보를 get_json함수로 받아옴.
    user_data = request.get_json()

    # get_json을 통해 받아온 데이터의 각 정보들을 따로 추출
    user_id = user_data.get('user_id')
    user_pw = user_data.get('user_pw')

    existing_user = db.account.find_one({'user_id': user_id})
    print("find user info: ", existing_user)
    if not existing_user:
        # userid가 존재하지 않는다면 400 리턴
        return jsonify({"status" : "fail", "message": "사용자 계정이 존재하지 않습니다."}), 400

    if existing_user['approved'] == False:
        # 계정 미승인 상태 400 리턴
        return jsonify({"status" : "fail", "message" : "회원가입 승인 대기상태입니다. 관리자에게 문의해주세요."})

    if existing_user['fail_count'] >= 5:
        # 패스워드를 5회 이상 틀린 경우 400 리턴
        return jsonify({"status" : "fail", "message" : "패스워드를 5회 이상 틀렸기 때문에 계정이 잠겼습니다. 관리자에게 문의해주세요."})

    # DB에 저장된 계정의 salt값 추출
    salt = existing_user['salt']
    # hash_password.py의 hash_password 함수를 호출하여 패스워드+솔트 값을 해싱한 결과를 받음
    hashed_password = hash_password(user_pw, salt)

    if not hashed_password == existing_user['user_pw']:
        # DB에 저장된 hashed password와 일치하지 않으면 fail_count를 1 증가시키고, 400리턴
        db.account.update_one({'_id': existing_user['_id']}, {'$inc': {'fail_count': 1}})
        return jsonify({"status" : "fail", "message" : "패스워드가 일치하지 않습니다."}), 400

    # 로그인 성공
    # DB에 저장된 fail_count를 0으로 초기화
    db.account.update_one({'_id': existing_user['_id']}, {'$set': {'fail_count': 0}})
    # jwt token 생성
    jwt_token = jwt.encode({
            'user_name' : existing_user['user_name'],
            'user_id': user_id,
            'google_otp_auth': False,
            'authority' : "None",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 토큰 유효 기간 설정
        }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({"status" : "success", "message" : "로그인 성공", "token" : jwt_token})