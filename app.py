from flask import Flask
from socket_instance import socketio
from views.user.signin_view import signin_blueprint
from views.user.signup_view import signup_blueprint
from views.user.find_id_view import find_id_blueprint
from views.user.find_pw_view import find_pw_blueprint
from views.user.dashboard_view import dashboard_blueprint
from views.user.linux_command_assistant_view import linux_command_assistant_blueprint
from views.user.linux_security_assistant_view import linux_security_assistant_blueprint
from views.user.mypage_view import mypage_blueprint
from views.admin.dashboard_view import admin_dashboard_blueprint
from views.admin.manage.user_view import user_manage_blueprint
from views.admin.manage.remote_view import remote_servers_blueprint
from views.user.linux_security_assistant_detail_view import linux_security_assistant_detail_blueprint
from views.admin.manage.logs_view import logs_view_blueprint
from views.admin.manage.evaluation_view import evaluation_view_blueprint
from views.API.account.signup_api import signup_api_blueprint
from views.API.account.signin_api import signin_api_blueprint
from views.API.account.get_users_api import get_users_api_blueprint
from views.API.find_id_api import find_id_api_blueprint
from views.API.find_pw_api import find_pw_api_blueprint
from views.API.linux_command_assistant.prompt import prompt_api_blueprint
from views.API.linux_command_assistant.terminal import terminal_socket_blueprint
from views.API.remote.remote_servers_api import remote_api_blueprint
from views.API.linux_security_assistant.policy import policy_api_blueprint
from views.API.linux_security_assistant.save_result import save_result_api_blueprint
from views.API.logs.logs_api import logs_api_blueprint
from views.API.logs.logs_dashboard_api import logs_dashboard_api_blueprint
from views.API.linux_command_assistant.check_input_api import check_input_api_blueprint
from views.API.account.dash_userinfo_api import dash_userinfo_api_blueprint
from views.API.mypage_api import mypage_api_blueprint


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
# linux_security_assistant Blueprint 경로: /views/user/linux_security_assistant_view.py
app.register_blueprint(linux_security_assistant_blueprint)
# Admin Dashboard Blueprint 경로: /views/admin/dashboard_view.py
app.register_blueprint(admin_dashboard_blueprint)
# User Manage Blueprint 경로: /views/admin/manage/user_view.py
app.register_blueprint(user_manage_blueprint)
# Remote Servers Manage Blueprint 경로: /views/admin/manage/remote_view.py
app.register_blueprint(remote_servers_blueprint)

# Logs View Blueprint 경로: /views/admin/manage/logs_view.py
app.register_blueprint(logs_view_blueprint)
# Linux Security Assistant Detail Blueprint 경로: /views/user/linux_security_assistant_detail_view.py
app.register_blueprint(linux_security_assistant_detail_blueprint)
# User evaluation view Blueprint 경로: /views/admin/manage/evaluation_view.py
app.register_blueprint(evaluation_view_blueprint)

# Mypage 경로: views/user/mypage_view.py
app.register_blueprint(mypage_blueprint)




""" API view blueprint """
# Signup Blueprint 경로: /views/API/account/signup_api.py
app.register_blueprint(signup_api_blueprint)
# Signin Blueprint 경로: /views/API/account/signin_api.py
app.register_blueprint(signin_api_blueprint)
# Get Users Blueprint 경로: /views/API/account/get_users_api.py
app.register_blueprint(get_users_api_blueprint)

# Find_id Blueprint 경로: /views/API/find_id_api.py
app.register_blueprint(find_id_api_blueprint)
# Find_pw Blueprint 경로: /views/API/find_pw_api.py
app.register_blueprint(find_pw_api_blueprint)

# Prompt API Blueprint 경로: /views/API/linux_command_assistant/prompt.py
app.register_blueprint(prompt_api_blueprint)

app.register_blueprint(terminal_socket_blueprint)


# Remote Server Blueprint 경뢰 /views/API/remote/remote_servers_api.py
app.register_blueprint(remote_api_blueprint)


app.register_blueprint(policy_api_blueprint)

app.register_blueprint(save_result_api_blueprint)

app.register_blueprint(logs_api_blueprint)

app.register_blueprint(logs_dashboard_api_blueprint)

# 터미널 질문 검사(토스트용) 추가: Prompt의 입력값 검사 Blueprint 경로: /views/API/linux_command_assistant/check_input.py
app.register_blueprint(check_input_api_blueprint)

# user/dashboard의 info 불러오기 경로: /views/API/account/dash_userinfo_api.py
app.register_blueprint(dash_userinfo_api_blueprint)

# Mypage Bluprint 경로: /views/API/mypage_api.py
app.register_blueprint(mypage_api_blueprint)





# app.py
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5009, debug=True)