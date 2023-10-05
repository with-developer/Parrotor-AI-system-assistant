from flask import Blueprint, render_template, jsonify

find_id_blueprint = Blueprint('find_id', __name__, url_prefix='/find_id')
# find_id root route: /find_id

@find_id_blueprint.route('/', methods=['GET', 'POST'])
def find_id():
    return render_template('user/find_id.html')