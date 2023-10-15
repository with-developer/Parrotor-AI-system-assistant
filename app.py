from flask import Flask, render_template, jsonify, request, session, redirect, url_for, current_app
from socket_instance import socketio
from views.user.signin_view import signin_blueprint
from views.user.signup_view import signup_blueprint
from views.user.find_id_view import find_id_blueprint
from views.user.find_pw_view import find_pw_blueprint
from views.user.dashboard_view import dashboard_blueprint
from views.user.linux_command_assistant_view import linux_command_assistant_blueprint
from views.admin.dashboard_view import admin_dashboard_blueprint
from views.admin.manage.user_view import user_manage_blueprint
from views.admin.manage.remote_view import remote_servers_blueprint
from views.API.account.signup_api import signup_api_blueprint
from views.API.account.signin_api import signin_api_blueprint
from views.API.account.get_users_api import get_users_api_blueprint
from views.API.linux_command_assistant.prompt import prompt_api_blueprint
from views.API.linux_command_assistant.terminal import terminal_socket_blueprint
from views.API.remote.remote_servers_api import remote_api_blueprint
from config import app

app = Flask(__name__)
socketio.init_app(app)

""" Default view blueprint """
# Signin Blueprint 경로: /views/user/signin_view.py
app.register_blueprint(signin_blueprint)
# Signup Blueprint 경로: /views/user/signup_view.py
app.register_blueprint(signup_blueprint)
# Find ID Blueprint 경로: /views/user/find_id_view.py
app.register_blueprint(find_id_blueprint)
# Find PW Blueprint 경로: /views/user/find_pw_view.py
app.register_blueprint(find_pw_blueprint)
# Dashboard Blueprint 경로: /views/user/dashboard_view.py
app.register_blueprint(dashboard_blueprint)
# linux_command_assistant Blueprint 경로: /views/user/linux_command_assistant_view.py
app.register_blueprint(linux_command_assistant_blueprint)
# Admin Dashboard Blueprint 경로: /views/admin/dashboard_view.py
app.register_blueprint(admin_dashboard_blueprint)
# User Manage Blueprint 경로: /views/admin/manage/user_view.py
app.register_blueprint(user_manage_blueprint)
# Remote Servers Manage Blueprint 경로: /views/admin/manage/remote_view.py
app.register_blueprint(remote_servers_blueprint)


""" API view blueprint """
# Signup Blueprint 경로: /views/API/account/signup_api.py
app.register_blueprint(signup_api_blueprint)
# Signin Blueprint 경로: /views/API/account/signin_api.py
app.register_blueprint(signin_api_blueprint)
# Get Users Blueprint 경로: /views/API/account/get_users_api.py
app.register_blueprint(get_users_api_blueprint)
# Prompt API Blueprint 경로: /views/API/linux_command_assistant/prompt.py
app.register_blueprint(prompt_api_blueprint)

app.register_blueprint(terminal_socket_blueprint)
# Remote Server Blueprint 경뢰 /views/API/remote/remote_servers_api.py
app.register_blueprint(remote_api_blueprint)


# app.py
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5009, debug=True)