from flask import Blueprint, render_template, jsonify
from ..API.account.account_verification_api import check_verification

admin_dashboard_blueprint = Blueprint('admin_dashboard', __name__, url_prefix='/jiranistrator/dashboard')
# admin dashboard root route: /jiranistrator/dashboard

@admin_dashboard_blueprint.route('/', methods=['GET', 'POST'])
@check_verification(['admin'])
def signin():
    return render_template('admin/dashboard.html', page_title="관리자/대시보드")