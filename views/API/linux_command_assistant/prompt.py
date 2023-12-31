import os
import openai
import datetime
import time, re
from bson.objectid import ObjectId
from flask import Blueprint, render_template, request, Response, jsonify, stream_with_context, g
from ..db_utils import mongodb_connect
from ...API.account.account_verification_api import check_verification
from dotenv import load_dotenv
from collections import Counter

load_dotenv(verbose=True)
openai_api_key = os.getenv('openai_api_key')
openai.api_key = openai_api_key

db = mongodb_connect()

prompt_api_blueprint = Blueprint('prompt_api', __name__, url_prefix='/API/prompt')

# This Route: /API/prompt/
@prompt_api_blueprint.route('', methods=['POST'])
@check_verification(['user','admin'])
def prompt_api():
    data = request.json
    message = data.get("message", "")
    serverId = data.get("serverId", "")


    if serverId != "None":
        server_id_like = db.remote.find_one({'_id': ObjectId(serverId)})['server_info']['id_like']
        server_pretty_name = db.remote.find_one({'_id': ObjectId(serverId)})['server_info']['pretty_name']
        prompt_content = f"""
server info: {server_id_like} {server_pretty_name}
"""
    else:
        prompt_content = ""

    prompt_content += f"""
You are a senior Linux engineer. Please answer {message}.


Instructions:
- Level of Difficulty: Easily
- Target Audience: Junior Linux Engineer
- Note 1: If executable code is provided, please include it in the tag "```sh".
- Note 2: The environment in which you can enter commands is the CLI.
- Respond language: Korean
"""


    messages = [
        {"role": "system", "content": "You are a useful Linux system engineer."},
        {"role": "user", "content": prompt_content}
    ]

    def generate():
        total_answer = ""
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                temperature=0.5,
                stream=True
            )
            for chunk in response:
                answer = chunk.get('choices', [{}])[0].get('delta', {}).get('content', "")
                ascii_answer = ",".join(str(ord(char)) for char in answer)
                total_answer += answer
                time.sleep(0.05)
                print(f"data: {answer}")
                yield f"data: {ascii_answer}\n\n"
        except Exception as e:
            yield f"data: error: {str(e)}\n\n"
        db.log.insert_one(
            {
                "log_type": "Linux Command Assistant",
                "user_id": g.user_id,
                "question" : message,
                "answer" : total_answer,
                "time" : (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        combined_string = message + total_answer

        command_keys = db.commands.find_one()

        key_counts = Counter()
        for key in command_keys:
            key_counts[key] = len(re.findall(re.escape(key), combined_string))

        for key, count in key_counts.items():
            if count > 0:
                db.commands.update_one({'_id': command_keys['_id']}, {'$inc': {key: count}})

        command_level_updates = {f"command_level.{key}": count for key, count in key_counts.items()}
        db.account.update_one({"user_id": g.user_id}, {"$inc": command_level_updates})
        
    return Response(stream_with_context(generate()), content_type='text/event-stream')



# This Route: /API/prompt/security_assistant
@prompt_api_blueprint.route('/security_assistant', methods=['POST'])
@check_verification(['user','admin'])
def security_prompt_api():
    data = request.json
    message = data.get("message", "")
    serverId = data.get("serverId", "")
    policy_name = data.get("policy_name", "")

    policy_classification = None
    policy_detail = None

    documents = db.policy.find()
    for document in documents:
        for key, value in document.items():
            if isinstance(value, dict) and policy_name in value:
                policy_classification = key
                policy_detail = value[policy_name]
                break

        if policy_classification:
            break


    if serverId != "None":
        server_id_like = db.remote.find_one({'_id': ObjectId(serverId)})['server_info']['id_like']
        server_pretty_name = db.remote.find_one({'_id': ObjectId(serverId)})['server_info']['pretty_name']
        prompt_content = f"""
server info: {server_id_like} {server_pretty_name}
주요정보통신기반시설 취약점 진단 가이드라인 항목: {policy_name}
세부 내용: {policy_detail}
"""
    else:
        prompt_content = ""

    prompt_content += f"""
당신은 주요정보통신기반시설 취약점 진단 가이드라인에 대해 잘 알고있는 보안 엔지니어입니다. 다음의 질문에 답변을 해주세요.
질문: {message}


Instructions:
- Level of Difficulty: Easily
- Target Audience: Junior Security Engineer
- Note 1: If executable code is provided, please include it in the tag "```sh".
- Note 2: The environment in which you can enter commands is the CLI.
- Respond language: Korean
"""

    messages = [
        {"role": "system", "content": "당신은 한국의 주요정보통신기반시설 취약점 진단 가이드라인에 대해 잘 알고있는 어시스턴트입니다."},
        {"role": "user", "content": prompt_content}
    ]

    def generate():
        total_answer = ""
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                temperature=0.2,
                stream=True
            )
            for chunk in response:
                answer = chunk.get('choices', [{}])[0].get('delta', {}).get('content', "")
                ascii_answer = ",".join(str(ord(char)) for char in answer)
                total_answer += answer
                time.sleep(0.05)
                print(f"data: {answer}")
                yield f"data: {ascii_answer}\n\n"
        except Exception as e:
            yield f"data: error: {str(e)}\n\n"
        db.log.insert_one(
            {
                "log_type": "Linux Security Assistant",
                "user_id": g.user_id,
                "question" : message,
                "answer" : total_answer,
                "time" : (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        combined_string = message + total_answer

        command_keys = db.commands.find_one()

        key_counts = Counter()
        for key in command_keys:
            key_counts[key] = len(re.findall(re.escape(key), combined_string))

        for key, count in key_counts.items():
            if count > 0:
                db.commands.update_one({'_id': command_keys['_id']}, {'$inc': {key: count}})
        

    
    return Response(stream_with_context(generate()), content_type='text/event-stream')