from flask import Blueprint, render_template
from ...API.account.account_verification_api import check_verification

remote_servers_blueprint = Blueprint('remote_servers', __name__, url_prefix='/jiranistrator/remote_servers')
# user manage root route: /jiranistrator/remote_servers

@remote_servers_blueprint.route('/', methods=['GET', 'POST'])
@check_verification(['admin'])
def user_manage():
    return render_template('admin/manage/remote.html', page_title="관리자/원격서버관리")