from flask import Blueprint, render_template, request, jsonify
import hashlib
from pymongo import MongoClient

signup_api_blueprint = Blueprint('signup_api', __name__, url_prefix='/API/account')

# Setup DB
client = MongoClient('34.22.80.174', 27017)
db = client['jirangobie']

# This Route: /API/account/signup
@signup_api_blueprint.route('/signup', methods=['POST'])
def signup_api():
    """ TODO
    1. userid가 동일한 계정이 존재하는지 체크: 완료
    2. userpw와 userpw_check가 동일한지 체크: 완료
    3. DB에 `name` , `userid` , `userpw` , `approve` , `fail_count` 값을 넣음.: 완료 
        주의사항 1: approve 초기값은 False. 담당자가 승인해줄 경우 True로 변경
        주의사항 2: userpw는  sha256으로 해싱하여 저장: 완료
        주의사항 3: userpw에 솔트값 추가해야함.: 해야함
        주의사항 4: fail_count는 초기값 0. 로그인 시 패스워드가 틀렸을 경우 1씩 증가하며, 5보다 같거나 클 경우 로그인 제한
    4. Google OTP qrcode 제공
    """
    user_data = request.get_json()
    
    # 전송받은 데이터를 로그로 출력합니다.
    print("Received data:", user_data)
    user_name = user_data.get('user_name')
    user_id = user_data.get('user_id')
    user_pw = user_data.get('user_pw')
    user_pw_check = user_data.get('user_pw_check')

    # 입력값 유효성 검증
    if len(user_name) >= 15:
        return jsonify({"status" : "fail", "message" : "사용자 이름이 15자 이상입니다."}), 400
    if len(user_id) >= 15:
        return jsonify({"status" : "fail", "message" : "사용자 아이디가 15자 이상입니다."}), 400
    if len(user_pw) <= 7:
        return jsonify({"status" : "fail", "message" : "사용자 비밀번호가 7자 이하입니다."}), 400
    if user_pw != user_pw_check:
        return jsonify({"status" : "fail", "message" : "사용자 비밀번호가 일치하지 않습니다."}), 400
    
    # 
    existing_user = db.account.find_one({'user_id': user_id})

    if existing_user:
        # 이미 userid가 존재하는 경우
        return jsonify({"status" : "fail", "message": "사용자 계정이 이미 존재합니다."}), 400
    else:
        # userid가 존재하지 않는 경우, 새로운 사용자를 등록합니다.
        sha256 = hashlib.sha256()
        sha256.update(user_pw.encode('utf-8'))
        hashed_password = sha256.hexdigest()
        print("hashed_password:", hashed_password)

        insert_data = {
            "user_name" : user_name,
            "user_id": user_id,
            "user_pw": hashed_password,
            "fail_count" : 0,
            "approved" : False,
            "google_otp_issue": False
        }
        db.account.insert_one(insert_data)
        return jsonify({"status" : "success", "message": "회원가입 요청 완료"}), 201

    return "nothing"