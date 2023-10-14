from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["fd"] = None
app.config["child_pid"] = None

app.config["ssh_client"] = None
app.config["ssh_channel"] = None