from flask import Blueprint, render_template
from ..API.account.account_verification_api import check_verification
from flask import g

linux_security_assistant_blueprint = Blueprint('linux_security_assistant', __name__, url_prefix='/linux_security_assistant')
# linux_security_assistant route: /linux_security_assistant

@linux_security_assistant_blueprint.route('/', methods=['GET'])
@check_verification(['user', 'admin'])
def linux_security_assistant():
    is_admin = True if g.user_role == "admin" else False
    return render_template('user/linux_security_assistant.html', page_title="리눅스 보안 어시스턴트", is_admin=is_admin)