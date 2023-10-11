import os
import urllib.parse

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('main2.html')

# #MongoDB connection
load_dotenv(verbose=True)

mongo_server_ip = os.getenv('mongo_server_ip')
mongo_server_port = int(os.getenv('mongo_server_port'))
mongo_account_db = os.getenv('mongo_account_db')
mongo_username = os.getenv('mongo_username')
mongo_password = os.getenv('mongo_password')

def mongodb_connect():
    username = urllib.parse.quote_plus(mongo_username)
    password = urllib.parse.quote_plus(mongo_password)

    connection_string = f"mongodb://{username}:{password}@{mongo_server_ip}:{mongo_server_port}/?authMechanism=DEFAULT"
    client = MongoClient(connection_string)
    db = client[mongo_account_db]
    return db



@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    # command와 correct 값이 제대로 제공되었는지 확인
    if not data or 'command' not in data or 'correct' not in data:
        return jsonify({"status": "error", "message": "Data format is incorrect."})

    db = mongodb_connect()

    # 제공된 데이터를 MongoDB에 저장
    try:
        db.commandlevel.insert_one(data)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database insertion error: {str(e)}"})

    return jsonify({"status": "success"})



