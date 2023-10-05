from flask import Blueprint, render_template
from ..API.account.account_verification_api import check_verification

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')
# dashboard root route: /

@dashboard_blueprint.route('/', methods=['GET'])
@check_verification(['user', 'admin'])
def signin():
    return render_template('user/dashboard.html')