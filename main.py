from ulearn import ULEARN
import pickle

ULEARN(username="41425243", password="")

with open("./cookies/41425243_20260619.pkl", "rb") as f:
    cookies = pickle.load(f)
    ULEARN(cookies=cookies)