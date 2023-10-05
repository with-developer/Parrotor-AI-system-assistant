from flask import Blueprint, request, jsonify
from ..db_utils import mongodb_connect
from .hash_password import hash_password
import re
import os
import base64


signup_api_blueprint = Blueprint('signup_api', __name__, url_prefix='/API/account')

db = mongodb_connect()

# This Route: /API/account/signup
@signup_api_blueprint.route('/signup', methods=['POST'])
def signup_api():
    """ TODO
    1. userid가 동일한 계정이 존재하는지 체크: 완료
    2. userpw와 userpw_check가 동일한지 체크: 완료
    3. DB에 `name` , `userid` , `userpw` , `approve` , `fail_count` 값을 넣음.: 완료 
        주의사항 1: approve 초기값은 False. 담당자가 승인해줄 경우 True로 변경
        주의사항 2: userpw는  sha256으로 해싱하여 저장: 완료
        주의사항 3: userpw에 솔트값 추가해야함.: 완료
        주의사항 4: fail_count는 초기값 0. 로그인 시 패스워드가 틀렸을 경우 1씩 증가하며, 5보다 같거나 클 경우 로그인 제한
    4. Google OTP qrcode 제공
    """
    # FE에서 전송된 회원가입 정보를 get_json함수로 받아옴.
    user_data = request.get_json()
    
    # get_json을 통해 받아온 데이터의 각 정보들을 따로 추출
    user_name = user_data.get('user_name')
    user_id = user_data.get('user_id')
    user_pw = user_data.get('user_pw')
    user_pw_check = user_data.get('user_pw_check')

    # 패스워드 유효성 검증 (영문 소문자, 대문자, 숫자 섞어서 10자 이상)
    if len(user_pw) < 10 or \
        not re.search('[a-z]', user_pw) or \
        not re.search('[A-Z]', user_pw) or \
        not re.search('[0-9]', user_pw):
        return jsonify({"status": "fail", "message": "비밀번호는 영문 소문자, 대문자, 숫자를 섞어서 10자 이상이어야 합니다."}), 400
    
    # 사용자 이름 길이 검증 (15자 미만)
    if len(user_name) >= 15:
        return jsonify({"status" : "fail", "message" : "사용자 이름이 15자 이상입니다."}), 400
    # 사용자 아이디 길이 검증 (15자 미만)
    if len(user_id) >= 15:
        return jsonify({"status" : "fail", "message" : "사용자 아이디가 15자 이상입니다."}), 400
    # 두 개의 패스워드가 일치한지 검증
    if user_pw != user_pw_check:
        return jsonify({"status" : "fail", "message" : "사용자 비밀번호가 일치하지 않습니다."}), 400
    
    # 이미 존재하는 userid가 있는지 검증
    existing_user = db.account.find_one({'user_id': user_id})
    if existing_user:
        # 이미 존재하는 userid가 있다면 400 리턴
        return jsonify({"status" : "fail", "message": "사용자 계정이 이미 존재합니다."}), 400
    
    # userid가 존재하지 않는 경우, 새로운 사용자를 등록

    # 32자리 랜덤 솔트값 생성
    salt = base64.b64encode(os.urandom(32)).decode('utf-8')  # 32바이트 무작위 값 생성 후, base64로 인코딩
    
    # hash_password.py 파일의 hash_password 함수 호출
    hashed_password = hash_password(user_pw, salt)

    insert_data = {
        "user_name" : user_name,
        "user_id" : user_id,
        "user_pw" : hashed_password,
        "salt" : salt,
        "fail_count" : 0,
        "approved" : False,
        "role" : "user"
    }
    db.account.insert_one(insert_data)
    return jsonify({"status" : "success", "message": "회원가입 요청 완료"}), 201