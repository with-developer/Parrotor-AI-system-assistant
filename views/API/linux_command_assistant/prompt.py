import os
import openai
from flask import Blueprint, render_template, request, Response, jsonify, stream_with_context
from ..db_utils import mongodb_connect
from ...API.account.account_verification_api import check_verification
from dotenv import load_dotenv

load_dotenv(verbose=True)
openai_api_key = os.getenv('openai_api_key')
openai.api_key = openai_api_key

prompt_api_blueprint = Blueprint('prompt_api', __name__, url_prefix='/API/prompt')

# This Route: /API/prompt/
@prompt_api_blueprint.route('', methods=['POST'])
@check_verification(['user','admin'])
def prompt_api():
    """TODO
    1. 전송된 데이터를 수신
    2. openai API를 통해 질문 전송
    3. 스트림 형태로 답변을 반환
    """
    data = request.json
    message = data.get("message", "")
    print("message:", message)

    messages = [
        {"role": "system", "content": "You are a useful Linux system engineer."},
        {"role": "user", "content": message}
    ]

    def generate():
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
                print(ascii_answer)
                yield f"data: {ascii_answer}\n\n"
        except Exception as e:
            yield f"data: error: {str(e)}\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')
