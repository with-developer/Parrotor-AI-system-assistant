# PARROTOR AI system assistant

<div align="center">
   <img src="https://github.com/with-developer/Parrotor-AI-system-assistant/assets/50432821/e96e13c3-8659-4db5-b68b-3523b3687563" width="300" height="300">
</div>

# 생성형 AI 리눅스 명령어/보안 어시스턴트 PARROTOR
S-개발자 1기(2차) 보안 제품 개발 프로젝트  
팀: 지란고비 (김서연, 김주미, 남윤정, 이지희, 이준형)  
담당 멘토: 지란지교시큐리티 윤두식 대표님  
프로젝트 기간: 23.09.25 ~ 23.12.04  

## 프로젝트 소개
Openai-API의 GPT 모델을 통해 사용자들이 명령어와 보안 지식을 학습하고, 웹 기반 터미널을 통해 실제 서버에 명령어를 적용해봄으로서 주니어 엔지니어를 더 빠르게 성장시킬 수 있도록 하는 서비스입니다.  
사용자는 하나의 인터페이스에서 질의응답 및 테스트 서버에서 명령어를 시뮬레이션 하면서 학습할 수 있으며,  
관리자는 주니어 엔지니어들의 실력을 파악하여 업무 효율성을 높일 수 있습니다. 

## 주요 기능 1 리눅스 명령어 어시스턴트
![image](https://github.com/with-developer/Parrotor-AI-system-assistant/assets/50432821/c5d6abe8-001b-4404-ad97-bc45e9e69e32)

## 주요 기능 2 리눅스 보안 어시스턴트
![image](https://github.com/with-developer/Parrotor-AI-system-assistant/assets/50432821/c860c804-0e1e-425f-9fe8-3c7603464e44)

## 전체 시연 영상


## 서비스 아키텍처
<img width="1374" alt="스크린샷 2023-12-04 오전 11 38 15" src="https://github.com/with-developer/Parrotor-AI-system-assistant/assets/50432821/c03e0d94-c3ac-4f67-b55d-1ad45857186c">






---
## 시작 가이드
### Requirements
Python 3.11.5   
`pip3 install -r requirements.txt`  
  
  
### Installation
`git clone https://github.com/with-developer/Parrotor-AI-system-assistant.git`  
  
  
### .env file setup
```
mongo_server_ip='example'
mongo_server_port='example'
mongo_account_db='example'
mongo_username = 'example'
mongo_password = 'example'
SECRET_KEY='example'
openai_api_key='example'
```  
  
  
### Run
```python3
python3 -m venv venv
source venv/bin/activate
python3 app.py
```  

