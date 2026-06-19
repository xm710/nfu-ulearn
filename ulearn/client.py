from .auth import Auth

class ULEARN(Auth):
    def __init__(self, username=None, password=None, cookies=None):
        Auth.__init__(self)
        

        if (username and password): 
            self.login_by_account(username, password)
        elif (cookies):
            self.login_by_cookies(cookies)

        if (self.is_login_success()):
            print("login successed")
        else:
            print("login failed")