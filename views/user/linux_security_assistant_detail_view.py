from flask import Blueprint, render_template
from ..API.account.account_verification_api import check_verification
from flask import g, request
from ..API.db_utils import mongodb_connect

db = mongodb_connect()

linux_security_assistant_detail_blueprint = Blueprint('linux_security_assistant_detail', __name__, url_prefix='/linux_security_assistant/detail')
# linux_security_assistant route: /linux_security_assistant

@linux_security_assistant_detail_blueprint.route('/', methods=['GET'])
@check_verification(['user', 'admin'])
def linux_security_assistant_detail():
    is_admin = True if g.user_role == "admin" else False
    policy_param = request.args.get('policy')
    print("policy_param:",policy_param)
    
    """TODO
    1. policy_param 변수가 mongodb의 중첩 json 내에서 어떤 키 내부에 들어가있는지 파악(policy_classification라는 변수에 저장)
    2. policy_classification 내부의 policy_param 내부의 json값을 policy_detail이라는 변수에 저장
    """
    # MongoDB의 문서를 순회하여 policy_param을 찾는 부분
    policy_classification = None
    policy_detail = None

    documents = db.policy.find()
    for document in documents:
        for key, value in document.items():
            if isinstance(value, dict) and policy_param in value:
                policy_classification = key
                policy_detail = value[policy_param]
                break

        if policy_classification:
            break

    print("policy_classification:", policy_classification)
    print("policy_detail:", policy_detail)

    return render_template('user/linux_security_assistant_detail.html', page_title="리눅스 보안 어시스턴트", is_admin=is_admin, policy_classification=policy_classification,policy_name=policy_param, policy_detail=policy_detail)