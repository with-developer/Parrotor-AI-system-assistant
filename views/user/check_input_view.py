from flask import Blueprint, render_template, jsonify

check_input_blueprint = Blueprint('check_input', __name__, url_prefix='/check_input')
# check_input root route: /check_input

@check_input_blueprint.route('/', methods = ['POST'])
def check_input():
    return render_template('user/linux_command_assistant.html')