# jirangobie Project
지란고비 프로젝트

## 프로젝트 시작하기 
1. Project Clone   
1.1. Visual Studio Code 터미널창에서 아래 명령어 실행   
   `git clone https://github.com/with-developer/jirangobie.git`   

2. Python install   
2.1. [Python 3.11.5 version install](https://www.python.org/downloads/windows/)   
2.2. `python3 -V` 입력 시 Python 3.11.5 나오는지 확인   

3. Python venv setup   
3.1. python3 -m venv venv   
3.2. source venv/bin/activate   

4. Project setup   
4.1. `pip3 install -r requirements.txt` 실행하여 필수 라이브러리 다운로드   
4.2. python3 app.py


## Git 협업 가이드 (작성중) 
1. [중요]각자 본인의 브랜치에서 코드 작성 후 commit & push 하기 (코드 컨플릭트 방지)   
이름별로 총 5개의 브랜치를 만들어놨습니다.   
브랜치 변경 방법: `git checkout remotes/origin/이름 -t`   
브랜치 변경되었는지 확인하는 방법: `git status`
    ```plaintext
    On branch 이준형
    Your branch is up to date with 'origin/이준형'.
    ```
    push 하는 방법: `git push origin 브랜치명`

2. [중요]작업 시작하기 전 `git pull origin main` 명령어로 최신 코드 받은 뒤, 시작 (코드 컨플릭트 방지)   

3. 커밋 메세지는 가능한 한글로 작성하기.
4. 주석 꼼꼼하게 작성하기.




## 디렉터리 구조 (9월26일 기준)
```
├── README.md
├── app.py   [Flask 기본 앱]
├── requirements.txt   [Python 라이브러리 구성요소 모음]
├── static   [Flask에서 Image, CSS, Javascript를 관리하는 디렉터리]
│   ├── css   [CSS 디렉터리]
│   │   └── bootstrap   [Bootstrap css 디렉터리]
│   │       └── bootstrap.min.css   [Bootstrap css 파일] 
│   └── js   [Javascript 디렉터리]
│       └── bootstrap   [Bootstrap javascript 디렉터리]
│           └── bootstrap.bundle.min.js   [Bootstrap javascript 파일]
├── templates   [Flask에서 html 파일을 관리하는 디렉터리]
│   ├── admin   [관리자가 접속할 수 있는 디렉터리]
│   │   └── dashboard.html   [관리자용 대시보드]
│   └── user   [일반 사용자가 접속할 수 있는 디렉터리]
│       ├── dashboard.html   [일반 사용자용 대시보드]
│       ├── signin.html   [로그인 페이지]
│       └── signup.html   [회원가입 페이지]
└── views
    ├── API   [API 작업을 처리하기 위한 디렉터리]
    │   └── account   [계정 관련 API 처리 디렉터리]
    │       └── signup_api.py   [회원가입 API 파일]
    ├── __init__.py   [필요 없어 보이지만, 필요한 파일..]
    ├── admin   [관리자용 라우팅 디렉터리]
    │   └── __init__.py   [필요 없어 보이지만, 필요한 파일..]
    └── user   [사용자용 라우팅 디렉터리]
        ├── __init__.py   [필요 없어 보이지만, 필요한 파일..]
        ├── signin_view.py   [로그인 라우팅 파일]
        └── signup_view.py   [회원가입 라우팅 파일]
```