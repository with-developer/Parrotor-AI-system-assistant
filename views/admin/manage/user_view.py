from flask import Blueprint, render_template, jsonify
from ...API.account.account_verification_api import check_verification

user_manage_blueprint = Blueprint('user_manage', __name__, url_prefix='/jiranistrator/manage/user')
# user manage root route: /jiranistrator/manage/user

@user_manage_blueprint.route('/', methods=['GET', 'POST'])
@check_verification(['admin'])
def user_manage():
    return render_template('admin/manage/user.html')