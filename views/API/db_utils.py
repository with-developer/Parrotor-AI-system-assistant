# db_utils.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(verbose=True)

mongo_server_ip = os.getenv('mongo_server_ip')
mongo_server_port = int(os.getenv('mongo_server_port'))  # port should be an integer
mongo_account_db = os.getenv('mongo_account_db')

def mongodb_connect():
    client = MongoClient(mongo_server_ip, mongo_server_port)
    db = client[mongo_account_db]
    return db