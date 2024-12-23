import requests
import json
import yaml
import os
from datetime import datetime, timedelta
import time

class KISOpenAPI:
    def __init__(self, config_path='./config/config.yaml', token_file='token.json'):
        self.config_path = config_path
        self.token_file = token_file
        self.load_config()
        self.access_token = None
        self.access_token_expired = None
        self.load_token()

    def load_config(self):
        """Load API configuration from YAML file."""
        with open(self.config_path, encoding='UTF-8') as f:
            _cfg = yaml.load(f, Loader=yaml.FullLoader)
        self.APP_KEY = _cfg['APP_KEY']
        self.APP_SECRET = _cfg['APP_SECRET']
        self.URL_BASE = _cfg['URL_BASE']
        self.CANO = _cfg['CANO']
        self.ACNT_PRDT_CD = _cfg['ACNT_PRDT_CD']
        self.HTS_ID = _cfg['HTS_ID']

    def load_token(self):
        """Load token information from file if it exists."""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r', encoding='UTF-8') as f:
                token_data = json.load(f)
                self.access_token = token_data.get('access_token')
                token_expired_str = token_data.get('access_token_expired')
                if token_expired_str:
                    self.access_token_expired = datetime.strptime(token_expired_str, '%Y-%m-%d %H:%M:%S')
                else:
                    print("토큰 만료 시간 정보가 없습니다.")
        else:
            self.access_token = None
            self.access_token_expired = None

    def save_token(self):
        """Save current token information to file."""
        with open(self.token_file, 'w', encoding='UTF-8') as f:
            token_data = {
                'access_token': self.access_token,
                'access_token_expired': self.access_token_expired
            }
            json.dump(token_data, f, ensure_ascii=False, indent=4)

    def get_access_token(self):
        """Request a new access token."""
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET
        }
        PATH = "oauth2/tokenP"
        URL = f"{self.URL_BASE}/{PATH}"

        time.sleep(0.05)  # Prevent rate limits
        res = requests.post(URL, headers=headers, data=json.dumps(body))

        if res.status_code == 200:
            try:
                response_json = res.json()
                self.access_token = response_json.get("access_token")
                self.access_token_expired = response_json.get("access_token_token_expired")
                self.save_token()
                print("새로운 토큰 발급 완료.")
            except KeyError as e:
                print(f"토큰 발급 중 키 에러 발생: {e}")
                print(res.json())
        else:
            print("접근 토큰 발급 실패. 응답 코드:", res.status_code)
            print("응답 내용:", res.json())

    def get_token(self):
        """Retrieve a valid token, issuing a new one if necessary."""
        if self.access_token is None or datetime.now() >= self.access_token_expired:
            print("토큰이 만료되었거나 존재하지 않습니다. 새로 발급합니다.")
            self.get_access_token()
        else:
            print("기존 토큰을 사용합니다.")
        return self.access_token