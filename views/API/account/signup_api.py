from flask import Blueprint, request, jsonify
from ..db_utils import mongodb_connect
from .hash_password import hash_password
import re
import os
import base64


signup_api_blueprint = Blueprint('signup_api', __name__, url_prefix='/API/account')

db = mongodb_connect()

# This Route: /API/account/signup
@signup_api_blueprint.route('/signup', methods=['POST'])
def signup_api():
    """ TODO
    1. userid가 동일한 계정이 존재하는지 체크: 완료
    2. userpw와 userpw_check가 동일한지 체크: 완료
    3. DB에 `name` , `userid` , `userpw` , `approve` , `fail_count` 값을 넣음.: 완료 
        주의사항 1: approve 초기값은 False. 담당자가 승인해줄 경우 True로 변경
        주의사항 2: userpw는  sha256으로 해싱하여 저장: 완료
        주의사항 3: userpw에 솔트값 추가해야함.: 완료
        주의사항 4: fail_count는 초기값 0. 로그인 시 패스워드가 틀렸을 경우 1씩 증가하며, 5보다 같거나 클 경우 로그인 제한
    4. Google OTP qrcode 제공
    """
    # FE에서 전송된 회원가입 정보를 get_json함수로 받아옴.
    user_data = request.get_json()
    
    # get_json을 통해 받아온 데이터의 각 정보들을 따로 추출
    user_name = user_data.get('user_name')
    user_id = user_data.get('user_id')
    user_pw = user_data.get('user_pw')
    user_pw_check = user_data.get('user_pw_check')

    # 패스워드 유효성 검증 (영문 소문자, 대문자, 숫자 섞어서 10자 이상)
    if len(user_pw) < 10 or \
        not re.search('[a-z]', user_pw) or \
        not re.search('[A-Z]', user_pw) or \
        not re.search('[0-9]', user_pw):
        return jsonify({"status": "fail", "message": "비밀번호는 영문 소문자, 대문자, 숫자를 섞어서 10자 이상이어야 합니다."}), 400
    
    # 사용자 이름 길이 검증 (15자 미만)
    if len(user_name) >= 15:
        return jsonify({"status" : "fail", "message" : "사용자 이름이 15자 이상입니다."}), 400
    # 사용자 아이디 길이 검증 (15자 미만)
    if len(user_id) >= 15:
        return jsonify({"status" : "fail", "message" : "사용자 아이디가 15자 이상입니다."}), 400
    # 두 개의 패스워드가 일치한지 검증
    if user_pw != user_pw_check:
        return jsonify({"status" : "fail", "message" : "사용자 비밀번호가 일치하지 않습니다."}), 400
    
    # 이미 존재하는 userid가 있는지 검증
    existing_user = db.account.find_one({'user_id': user_id})
    if existing_user:
        # 이미 존재하는 userid가 있다면 400 리턴
        return jsonify({"status" : "fail", "message": "사용자 계정이 이미 존재합니다."}), 400
    
    # userid가 존재하지 않는 경우, 새로운 사용자를 등록

    # 32자리 랜덤 솔트값 생성
    salt = base64.b64encode(os.urandom(32)).decode('utf-8')  # 32바이트 무작위 값 생성 후, base64로 인코딩
    
    # hash_password.py 파일의 hash_password 함수 호출
    hashed_password = hash_password(user_pw, salt)

    insert_data = {
        "user_name" : user_name,
        "user_id" : user_id,
        "user_pw" : hashed_password,
        "salt" : salt,
        "fail_count" : 0,
        "approved" : False,
        "role" : "user",
        "lastlogin" : None,
        "command_level": {
            "ls": 0,
            "clear": 0,
            "cd": 0,
            "cat": 0,
            "touch": 0,
            "head": 0,
            "tail": 0,
            "echo": 0,
            "cal": 0,
            "df": 0,
            "bc": 0,
            "help": 0,
            "uname": 0,
            "factor": 0,
            "whatis": 0,
            "mkdir": 0,
            "who": 0,
            "gzip": 0,
            "free": 0,
            "finger": 0,
            "man": 0,
            "groups": 0,
            "w": 0,
            "passwd": 0,
            "history": 0,
            "whoami": 0,
            "cp": 0,
            "lscpu": 0,
            "top": 0,
            "mv": 0,
            "env": 0,
            "printenv": 0,
            "ps": 0,
            "hostname": 0,
            "rm": 0,
            "nano newFile": 0,
            "ip": 0,
            "curl": 0,
            "wget": 0,
            "last": 0,
            "yes": 0,
            "iostat": 0,
            "locate": 0,
            "shutdown": 0,
            "reboot": 0,
            "dir": 0,
            "apt install": 0,
            "apt remove": 0,
            "apt search": 0,
            "apt autoremove": 0,
            "apt update": 0,
            "apt upgrade": 0,
            "exit": 0,
            "paste": 0,
            "sort": 0,
            "tar": 0,
            "gunzip": 0,
            "zip": 0,
            "unzip": 0,
            "diff": 0,
            "hostnamectl": 0,
            "lsof": 0,
            "netstat": 0,
            "iptables": 0,
            "service": 0,
            "mpstat": 0,
            "vmstat": 0,
            "uniq": 0,
            "ncdu": 0,
            "stat": 0,
            "sleep": 0,
            "split": 0,
            "ping or": 0,
            "du": 0,
            "useradd": 0,
            "usermod": 0,
            "userdel": 0,
            "awk": 0,
            "dig": 0,
            "whereis": 0,
            "pstree": 0,
            "tree": 0,
            "printf": 0,
            "find": 0,
            "sed": 0,
            "rmdir": 0,
            "chown": 0,
            "lsblk": 0,
            "screen": 0,
            "chmod": 0,
            "grep": 0,
            "basename": 0,
            "which": 0,
            "wc": 0,
            "fdisk": 0,
            "date": 0,
            "tr": 0,
            "fold": 0,
            "zcat": 0,
            "parted": 0,
            "tac": 0,
            "neofetch": 0,
            "xeyes": 0,
            "su": 0,
            "ln -s": 0,
            "xdg-open": 0,
            "cmp": 0,
            "comm": 0,
            "less": 0,
            "vi": 0,
            "kill": 0,
            "killall": 0,
            "jobs": 0,
            "bg": 0,
            "fg": 0,
            "export": 0,
            "crontab": 0,
            "alias": 0,
            "unalias": 0,
            "dnf install": 0,
            "pacman -S": 0,
            "snap install": 0,
            "flatpak install": 0,
            "htop": 0,
            "ip addr": 0,
            "ifconfig": 0,
            "ssh": 0,
            "mount": 0,
            "umount": 0,
            "pwconv": 0,
            "pwunconv": 0,
            "chgrp": 0,
            "groupadd": 0,
            "rsh": 0,
            "rlogin": 0,
            "rexec": 0,
            "inetadm": 0,
            "umask": 0,
            "rmuser": 0,
            "ftp": 0,
            "telnet": 0
        }
    }
    db.account.insert_one(insert_data)
    return jsonify({"status" : "success", "message": "회원가입 요청 완료"}), 201