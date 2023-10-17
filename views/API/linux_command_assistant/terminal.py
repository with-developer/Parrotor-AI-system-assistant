from flask import Blueprint
from config import app as global_app
from socket_instance import socketio
from ...API.account.account_verification_api import check_verification
import paramiko
import termios
import struct
import fcntl


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

@socketio.on("pty-init", namespace="/API/terminal/pty")
@check_verification(['user', 'admin'])
def pty_input(data):
    if global_app.config["ssh_channel"]:
        print("Init channel")
        global_app.config["ssh_channel"].send('\n')


@socketio.on("resize", namespace="/API/terminal/pty")
@check_verification(['user', 'admin'])
def resize(data):
    if global_app.config["fd"]:
        print(f"Resizing window to {data['rows']}x{data['cols']}")
        set_winsize(global_app.config["fd"], data["rows"], data["cols"])


@socketio.on("connect", namespace="/API/terminal/pty")
@check_verification(['user', 'admin'])
def connect():
    print("new client connected")
    if global_app.config["ssh_channel"]:
        return

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect("127.0.0.1", port=5006, username="user2", password="1234")

    ssh_channel = ssh_client.invoke_shell(term="xterm-color")

    global_app.config["ssh_client"] = ssh_client
    global_app.config["ssh_channel"] = ssh_channel
    

    socketio.start_background_task(target=read_and_forward_ssh_output)

    print("SSH channel created")
    print("starting background task to continuously read and forward SSH output to client")
    print("task started")
