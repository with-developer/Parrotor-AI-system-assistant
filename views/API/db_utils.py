# db_utils.py
import os
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

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