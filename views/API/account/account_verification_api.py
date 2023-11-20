import jwt
import os
from functools import wraps
from flask import request, render_template
from dotenv import load_dotenv
from flask import g

load_dotenv(verbose=True)
SECRET_KEY = os.getenv('SECRET_KEY')

def check_verification(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.cookies.get('access_token')
            if not token:
                return render_template('alert_and_redirect.html', message="로그인을 먼저 해주세요.", redirect_url="/")
            
            try:
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                current_user_role = decoded_token.get('role', None)
                current_user_id = decoded_token.get('user_id', None)
                current_user_name = decoded_token.get('user_name', None)
            except jwt.ExpiredSignatureError:
                return render_template('alert_and_redirect.html', message="토큰이 만료되었습니다.", redirect_url="/")
            except jwt.InvalidTokenError:
                return render_template('alert_and_redirect.html', message="잘못된 토큰입니다.", redirect_url="/")
            
            if current_user_role not in required_roles:
                print(request.referrer)
                return render_template('alert_and_redirect.html', message="권한이 없습니다.", redirect_url=request.referrer or "/")
            
            g.user_role = current_user_role
            g.user_id = current_user_id
            g.user_name = current_user_name
            return f(*args, **kwargs)
        return decorated_function
    return decorator
