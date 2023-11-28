from flask import Blueprint, render_template
from ..API.account.account_verification_api import check_verification
from flask import g

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')
# dashboard root route: /

@dashboard_blueprint.route('/', methods=['GET'])
@check_verification(['user', 'admin'])
def signin():
    is_admin = True if g.user_role == "admin" else False
    return render_template('user/dashboard.html', page_title="대시보드", is_admin=is_admin)