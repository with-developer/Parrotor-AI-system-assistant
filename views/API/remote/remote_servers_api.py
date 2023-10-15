from flask import Blueprint, request, jsonify
from ..db_utils import mongodb_connect
import re
import os
import base64
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
            'os': server_info['os'],
            'version': server_info['version'],
            'ip_address' : server_info['ip_address'],
            'saved_script' : server_info['saved_script'],
            'last_scan' : server_info['last_scan'],
        }
    print("servers:",filtered_servers)

    return jsonify({"status" : "success", "message": "원격 서버 조회 성공", "servers": filtered_servers, "total_pages": total_pages, "total_servers": total_servers}), 201

# This Route: /API/remote/get-servers
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

    return jsonify({"status" : "success", "message": "원격 서버 추가 성공"}), 201