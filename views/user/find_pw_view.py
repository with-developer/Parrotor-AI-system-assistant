from flask import Blueprint, render_template, jsonify

find_pw_blueprint = Blueprint('find_pw', __name__, url_prefix='/find_pw')
# find_id root route: /find_pw

@find_pw_blueprint.route('/', methods=['GET', 'POST'])
def find_pw():
    return render_template('user/find_pw.html')