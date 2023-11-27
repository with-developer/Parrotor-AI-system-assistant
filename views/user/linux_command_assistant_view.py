from flask import Blueprint, render_template
from ..API.account.account_verification_api import check_verification
from flask import g

linux_command_assistant_blueprint = Blueprint('linux_command_assistant', __name__, url_prefix='/linux_command_assistant')
# dashboard root route: /

@linux_command_assistant_blueprint.route('/', methods=['GET'])
@check_verification(['user', 'admin'])
def linux_command_assistant():
    is_admin = True if g.user_role == "admin" else False
    return render_template('user/linux_command_assistant.html', page_title="리눅스 명령어 어시스턴트", is_admin=is_admin)