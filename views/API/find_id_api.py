from flask import Blueprint, render_template, request, jsonify
from .db_utils import mongodb_connect
from dotenv import load_dotenv
import os

find_id_api_blueprint = Blueprint('find_id_api', __name__, url_prefix='/API/find_id')

db = mongodb_connect()

load_dotenv(verbose=True)
SECRET_KEY = os.getenv('SECRET_KEY')

#This is Route: /API/find_id
@find_id_api_blueprint.route('/', methods=['POST'])
def find_id_api():
    """ TODO
    1. user_name과 더불어 user_email도 받아오기
    """
    # FE에서 전송된 회원가입 정보를 get_json 함수로 받아옴
    user_data = request.get_json()
    # get_json을 통해 받아온 데이터의 각 정보들을 따로 추출
    user_name = user_data.get('user_name')
    # user_name으로 해당 사용자의 user_info를 검색
    user_info = db.account.find_one({'user_name': user_name})

    # 존재하지 않는 사용자라면 400 리턴
    if not user_info:
        return jsonify({"status" : "fail", "message": "해당 이름의 사용자 계정이 존재하지 않습니다."}), 400

    # 사용자가 존재하는 경우
    user_id = user_info.get('user_id')
    
    # user_id의 첫 3자만 가져오고 나머지는 *로 변환
    masked_user_id = user_id[:3] + '*'*(len(user_id)-3)

    return jsonify({"status":"success", "masked_user_id":masked_user_id}), 200
    