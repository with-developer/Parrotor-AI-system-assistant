from flask import Blueprint, render_template, jsonify

signup_blueprint = Blueprint('signup', __name__, url_prefix='/signup')
# signin root route: /signup

@signup_blueprint.route('/', methods=['GET', 'POST'])
def signup():
    return render_template('user/signup.html')