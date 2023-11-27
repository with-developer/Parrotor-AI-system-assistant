from flask import Blueprint, render_template, jsonify
from ...API.account.account_verification_api import check_verification

logs_view_blueprint = Blueprint('logs_view', __name__, url_prefix='/jiranistrator/logs')
# user manage root route: /jiranistrator/manage/user

@logs_view_blueprint.route('/', methods=['GET', 'POST'])
@check_verification(['admin'])
def logs_view():
    return render_template('admin/manage/logs.html', page_title="관리자/사용자 추적")