from flask import Blueprint, render_template, jsonify
from ...API.account.account_verification_api import check_verification

evaluation_view_blueprint = Blueprint('evaluation_view', __name__, url_prefix='/jiranistrator/evaluation')
# user manage root route: /jiranistrator/manage/user

@evaluation_view_blueprint.route('/', methods=['GET', 'POST'])
@check_verification(['admin'])
def evaluation_view():
    return render_template('admin/manage/evaluation.html', page_title="관리자/사용자 평가")