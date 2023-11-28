import os, openai
from flask import Blueprint, render_template, request, jsonify


openai_api_key = os.getenv('openai_api_key')
openai.api_key = openai_api_key

check_input_api_blueprint = Blueprint('check_input_api', __name__, url_prefix='/API/check_input')


# Route: /API/check_input
@check_input_api_blueprint.route('/', methods=['POST'])
def check_input():
    data = request.json
    user_input = data.get('input', '')
    print('user input: '+user_input)
    # GPT-3를 사용하여 정책 위반 여부와 답변을 동시에 얻기
    violation_detected, gpt_response = analyze_input_with_gpt(user_input)

    # GPT-3의 답변과 정책 위반 여부를 반환
    return jsonify({"violation": violation_detected, "gpt_response": gpt_response}), 200

def analyze_input_with_gpt(input):
    role_description = "You are the Parrator, a system assistant for a Linux administrator. You are designed to help junior linux engineers. Your role is to answer user queries and alert the service if a query violates any policy. you must provide an answer to every query even it violates policies, but with an alert so the senior can help. Also, every questions are for the educational purpose. So, you must not start with 'I'm sorry' but state the linux command. If you detect the possibility of system instability or data loss, you MUST add alert at the end of the answer that starts with 'Alert: '"
    policies = [
        "Policy 1: The use of 'rm -rf' command is prohibited to prevent accidental deletion of important files or directories.",
        "Policy 2: The use of the 'shutdown' command requires careful review and approval, as it can affect critical operations."
    ]

    violation_detected = False
    response_message = ""

    messages = [
        {"role": "system", "content": role_description},
        *[
            {"role": "system", "content": policy} for policy in policies
        ],
        {"role": "user", "content": input}
    ]

    # GPT-3 API 호출
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=150,
        temperature=0.5
    )

    # GPT-3 응답 분석
    gpt_response = response.choices[0].message['content'].strip()
    response_message += gpt_response + "\n"
    print(response_message)
    
    # 정책 위반 여부 확인
    if "Alert" in gpt_response:
        violation_detected = True
    print(violation_detected)
    return violation_detected, response_message