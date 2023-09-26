from flask import Flask, render_template, jsonify, request, session, redirect, url_for, current_app
from views.user.signin_view import signin_blueprint
from views.user.signup_view import signup_blueprint

app = Flask(__name__)
app.register_blueprint(signin_blueprint)
# Signin Blueprint 경로: /views/user/signin.py
app.register_blueprint(signup_blueprint)
# Signup Blueprint 경로: /views/user/signup.py



# app.py
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5009, debug=True)