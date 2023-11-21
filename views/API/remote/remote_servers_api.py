from flask import Blueprint, request, jsonify, g
from ..db_utils import mongodb_connect
import paramiko
from ...API.account.account_verification_api import check_verification


remote_api_blueprint = Blueprint('remote_api', __name__, url_prefix='/API/remote')

db = mongodb_connect()

# This Route: /API/remote/get-servers
@remote_api_blueprint.route('/get-servers', methods=['POST'])
@check_verification(['admin'])
def get_servers():
    page = int(request.form.get('page', 1))
    items_per_page = 10
    skip = (page - 1) * items_per_page
    
    total_servers = db.remote.count_documents({})
    total_pages = -(-total_servers // items_per_page)  # 올림 나눗셈

    servers = {server['_id']: server for server in db.remote.find().skip(skip).limit(items_per_page)}
    filtered_servers = {}
    for server_id, server_info in servers.items():
        filtered_servers[str(server_id)] = {
            'server_name': server_info['server_name'],
            'security_score': server_info['security_score'],
            'access_role': server_info['access_role'],
            'os': server_info['server_info']['id'],
            'version': server_info['server_info']['version'],
            'ip_address' : server_info['server_ip'],
            'saved_script' : server_info['saved_script'],
            'last_scan' : server_info['last_scan'],
        }
    print("servers:",filtered_servers)

    # 사용자 권한 가져오기
    role_data = db.user_role.find()
    roles = [roles['role'] for roles in role_data][0]


    return jsonify({"status" : "success", "message": "원격 서버 조회 성공", "servers": filtered_servers, "total_pages": total_pages, "total_servers": total_servers, "roles" : roles}), 201

# This Route: /API/remote/get-servers-name
@remote_api_blueprint.route('/get-servers-name', methods=['GET'])
@check_verification(['user', 'admin'])
def get_servers_name():

    print(g.user_role)
    # if role이 admin이라면 모든 서버 다 출력, 아니라면 해당 권한에 맞는 서버만 출력
    if g.user_role == 'admin':
        servers = {server['_id']: server for server in db.remote.find()}
    else:
        servers = {server['_id']: server for server in db.remote.find({"access_role" : g.user_role })}

    filtered_servers = {}
    for server_id, server_info in servers.items():
        filtered_servers[str(server_id)] = {
            'id': str(server_info["_id"]),
            'server_name': server_info['server_name']
        }
    print("servers:",filtered_servers)


    return jsonify({"status" : "success", "message": "원격 서버 조회 성공", "servers": filtered_servers}), 201
    

# This Route: /API/remote/add-remote-server
@remote_api_blueprint.route('/add-remote-server', methods=['POST'])
@check_verification(['admin'])
def add_remote_server():
    """
    TODO
    1. ajax를 통해 받은 값 변수로 저장
    2. 해당 정보를 통해 paramiko ssh 연결
    3. ssh 채널로 서버 정보를 얻어옴(/etc/issue)
    4. 성공시 DB에 값들 저장
    4.1. 실패시 해당 에러 반환
    """
    # Get ajax json
    server_name = request.json.get('server_name')
    access_role = request.json.get('access_role')
    print(access_role)
    server_ip = request.json.get('server_ip')
    server_port = request.json.get('server_port')
    username = request.json.get('username')
    password = request.json.get('password')

    # 각 변수마다 검증 로직이 필요함. ip의 경우 정규표현식, 포트번호 int 맞는지

    # SSH 클라이언트 객체 생성
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 원격 서버에 접속
        client.connect(server_ip, port=server_port, username=username, password=password)
    except Exception as e:
        return jsonify({"status" : "fail", "message" : "원격 서버에 접속할 수 없습니다."})

    # 원격 서버에서 실행할 명령
    command = "cat /etc/os-release"
    stdin, stdout, stderr = client.exec_command(command)

    # 결과 가져오기
    result = [item.strip() for item in stdout.readlines()[:6]]
    result_err = stderr.readlines()

    # 접속 종료
    client.close()

    if result_err:
        print("[!] SSH exec command error:", result_err)
        return jsonify({"status" : "fail", "message" : "서버에 연결했지만, 정보를 가져올 수 없습니다."})

    def extract_value(data, index):
        try:
            return data[index].split('=')[1].strip('"')
        except Exception:
            return "unknown"

    insert_data = {
        "server_name" : server_name,
        "access_role" : access_role,
        "server_ip" : server_ip,
        "server_port" : int(server_port),
        "username" : username,
        "password" : password,
        "security_score" : "unknown",
        "saved_script" : "not saved",
        "last_scan" : "not yet",
        "server_info" : {
            "name" : extract_value(result, 0),
            "version" : extract_value(result, 1),
            "id" : extract_value(result, 2),
            "id_like" : extract_value(result, 3),
            "pretty_name" : extract_value(result, 4),
            "version_id" : extract_value(result, 5),
            }
    }
    db.remote.insert_one(insert_data)


    return jsonify({"status" : "success", "message": "원격 서버 추가 성공"}), 201