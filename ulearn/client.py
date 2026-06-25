from .auth import Auth
from .types import Todo

class ULEARN(Auth):
    def __init__(self, username=None, password=None, cookies=None):
        Auth.__init__(self)
        

        if (username and password): 
            self.login_by_account(username, password)
        elif (cookies):
            self.login_by_cookies(cookies)

        if (self._is_login_success()):
            print("login successed")
        else:
            print("login failed")

    def get_todo_list(self, print_=False):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": None,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        }
        
        data = self._session.get(
            url = "https://ulearn.nfu.edu.tw/api/todos?no-intercept=true",
            headers = headers
        ).json().get("todo_list")

        if (print_):
            for d in data:
                print(Todo(d), end="\n\n")

