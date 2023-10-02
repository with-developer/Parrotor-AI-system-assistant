from flask import Flask, render_template, jsonify, request, session, redirect, url_for, current_app
from views.user.signin_view import signin_blueprint
from views.user.signup_view import signup_blueprint
from views.user.dashboard_view import dashboard_blueprint
from views.admin.dashboard_view import admin_dashboard_blueprint
from views.API.account.signup_api import signup_api_blueprint
from views.API.account.signin_api import signin_api_blueprint

app = Flask(__name__)

""" Default view blueprint """
# Signin Blueprint 경로: /views/user/signin_view.py
app.register_blueprint(signin_blueprint)
# Signup Blueprint 경로: /views/user/signup_view.py
app.register_blueprint(signup_blueprint)
# Dashboard Blueprint 경로: /views/user/dashboard_view.py
app.register_blueprint(dashboard_blueprint)
# Admin Dashboard Blueprint 경로: /views/admin/dashboard_view.py
app.register_blueprint(admin_dashboard_blueprint)

""" API view blueprint """
# Signup Blueprint 경로: /views/API/account/signup_api.py
app.register_blueprint(signup_api_blueprint)
# Signin Blueprint 경로: /views/API/account/signin_api.py
app.register_blueprint(signin_api_blueprint)


# app.py
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5009, debug=True)