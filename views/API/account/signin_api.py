from flask import Blueprint, render_template
from hashlib import sha256

signin_api_blueprint = Blueprint('signin_api', __name__, url_prefix='/API/account')

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
    return "nothing"