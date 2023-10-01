from flask import Blueprint, render_template, jsonify

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')
# signin root route: /

@dashboard_blueprint.route('/', methods=['GET', 'POST'])
def signin():
    return render_template('user/dashboard.html')