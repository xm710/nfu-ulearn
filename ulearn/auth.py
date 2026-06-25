import ssl
import pickle
import datetime
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

from .UI import Captcha

class BypassStrictAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()

        # 跳過 SSL 驗證錯誤
        context.verify_flags &= ~ssl.VERIFY_X509_STRICT
        
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)
    
class URL:
    IDENTITY = "https://identity.nfu.edu.tw"
    LOGIN    = IDENTITY +                 "/auth/realms/nfu/protocol/cas/login?service=https://ulearn.nfu.edu.tw/login"
    CODE     = IDENTITY +                 "/auth/realms/nfu/captcha/code"

    INDEX = "https://ulearn.nfu.edu.tw/user/index#/"

class Auth:
    def __init__(self):
        self._session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        self._session.mount('https://', BypassStrictAdapter())

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-TW,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        }

        self._session.headers.update(headers)

    def login_by_account(self, username, password):
        response = self._session.get(URL.LOGIN)

        authenticateURL = BeautifulSoup(response.text, "html.parser").find("form", class_="form-horizontal").get("action")
        captchaCode = self._get_captcha_code()
        inputCode = Captcha(captchaCode.get("CaptchaData")).show()
        data = {
            "username"   : username, # 學號
            "password"   : password, # 密碼
            "captchaCode": inputCode,
            "captchaKey" : captchaCode.get("CaptchaKey"),
        }

        response = self._session.post(
            url=authenticateURL,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            allow_redirects=True,
        )

        with open(f"./cookies/{username}_{datetime.datetime.now().strftime('%Y%m%d')}.pkl", "wb") as f:
            pickle.dump(self._session.cookies, f)

    def login_by_cookies(self, cookies):
        self._session.cookies.update(cookies)

    def _get_captcha_code(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": None,
            "X-Requested-With": "XMLHttpRequest",
        }

        data = self._session.get(
            url=URL.CODE,
            headers=headers
        ).json()
        
        return {
            "CaptchaData": data.get("image").split(",")[1],
            "CaptchaKey": data.get("key"),
        }
    
    def _is_login_success(self):
        response = self._session.get(
            URL.INDEX,
            allow_redirects=False
        )

        return (response.status_code == 200)