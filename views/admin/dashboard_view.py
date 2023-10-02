from flask import Blueprint, render_template, jsonify

admin_dashboard_blueprint = Blueprint('admin_dashboard', __name__, url_prefix='/jiranistrator/dashboard')
# admin dashboard root route: /

@admin_dashboard_blueprint.route('/', methods=['GET', 'POST'])
def signin():
    return render_template('admin/dashboard.html')