from flask import Blueprint, render_template, jsonify

mypage_blueprint = Blueprint('mypage', __name__, url_prefix='/dashboard/mypage')
# mypage root route: dashboard/mypage

@mypage_blueprint.route('/', methods=['GET','POST'])
def mypage():
    return render_template('user/mypage.html')