from flask import Blueprint, g, jsonify
from config import app as global_app
from socket_instance import socketio
from ...API.account.account_verification_api import check_verification
import paramiko
import termios
import struct
import fcntl
from bson.objectid import ObjectId
from ..db_utils import mongodb_connect

db = mongodb_connect()

terminal_socket_blueprint = Blueprint('terminal_socket', __name__, url_prefix='/API/terminal')

def set_winsize(fd, row, col, xpix=0, ypix=0):
    print("setting window size with termios")
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_ssh_output():
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if "ssh_channel" in global_app.config and global_app.config["ssh_channel"]:
            if global_app.config["ssh_channel"].recv_ready():
                output = global_app.config["ssh_channel"].recv(max_read_bytes).decode(errors="ignore")
                
                socketio.emit("pty-output", {"output": output}, namespace="/API/terminal/pty")

@socketio.on("pty-input", namespace="/API/terminal/pty")
@check_verification(['user', 'admin'])
def pty_input(data):
    if global_app.config["ssh_channel"]:
        print("received input from browser: %s" % data["input"])
        global_app.config["ssh_channel"].send(data["input"])

# @socketio.on("pty-init", namespace="/API/terminal/pty")
# @check_verification(['user', 'admin'])
# def pty_input(data):
#     if global_app.config["ssh_channel"]:
#         print("Init channel")
#         global_app.config["ssh_channel"].send('\n')


@socketio.on("resize", namespace="/API/terminal/pty")
@check_verification(['user', 'admin'])
def resize(data):
    if global_app.config["fd"]:
        print(f"Resizing window to {data['rows']}x{data['cols']}")
        set_winsize(global_app.config["fd"], data["rows"], data["cols"])


@socketio.on("connect-server", namespace="/API/terminal/pty")
@check_verification(['user', 'admin'])
def connect(server_id):
    print("new client connected")
    print("server_id:",server_id)
    """TODO
    1. DB에서 해당 server_id 권한 가져오기
    2. 권한 확인하기
    2.T. 권한 일치한다면 port, username, password 가져오기
    2.T. 서버 연결
    2.F. 권한 일치하지 않는다면 403 리턴
    """
    server_info = db.remote.find_one({'_id': ObjectId(server_id)})
    print(server_info['access_role'])
    if g.user_role in server_info['access_role']:
        server_ip = server_info['server_ip']
        server_port = server_info['server_port']
        server_username = server_info['username']
        server_password = server_info['password']
    else:
        return jsonify({"status":"fail", "message":"서버 권한이 일치하지 않습니다."}), 403
    if global_app.config["ssh_channel"]:
        global_app.config["ssh_channel"].close()
        global_app.config["ssh_client"].close()

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(server_ip, port=int(server_port), username=server_username, password=server_password)

    ssh_channel = ssh_client.invoke_shell(term="xterm-color")

    global_app.config["ssh_client"] = ssh_client
    global_app.config["ssh_channel"] = ssh_channel
    

    socketio.start_background_task(target=read_and_forward_ssh_output)

    print("SSH channel created")
    print("starting background task to continuously read and forward SSH output to client")
    print("task started")

@socketio.on("disconnect", namespace="/API/terminal/pty")
def handle_disconnect():
    print("Client disconnected")
    if "ssh_channel" in global_app.config and global_app.config["ssh_channel"]:
        global_app.config["ssh_channel"].close()
        print("SSH channel closed")
    if "ssh_client" in global_app.config and global_app.config["ssh_client"]:
        global_app.config["ssh_client"].close()
        print("SSH client closed")