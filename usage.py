from ulearn import ULEARN
import pickle

# 1. 帳密登入
ULEARN(username="學號", password="密碼")


# 2. 憑證登入
with open("./cookies/41425243_20260619.pkl", "rb") as f:
    cookies = pickle.load(f)
    ULEARN(cookies=cookies)