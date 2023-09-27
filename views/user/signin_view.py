from flask import Blueprint, render_template, jsonify

signin_blueprint = Blueprint('signin', __name__, url_prefix='/')
# signin root route: /

@signin_blueprint.route('/', methods=['GET', 'POST'])
def signin():
    return render_template('user/signin.html')