import json
import pickle

import urllib3
import requests
from requests.cookies import cookiejar_from_dict, merge_cookies

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"


def new_session(proxy=None, user_agent=None, verify=False):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    s = requests.session()
    if proxy:
        s.proxies = {
            'http': proxy,
            'https': proxy,
        }
    if user_agent:
        s.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36',
        }
    s.verify = verify
    return s


def save_session(s, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(s, f)


def read_session(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def dump_cookies(s, file_path):
    with open(file_path, 'w') as f:
        json.dump(requests.utils.dict_from_cookiejar(s.cookies), f, indent=4)


def load_cookies(s, file_path):
    with open(file_path, 'r') as f:
        return merge_cookies(s.cookies, json.load(f))


def load_cookies_formm_chrome_cookies_str(s, chrome_cookies_str):
    manual_cookies = {}
    for one in chrome_cookies_str.split(";"):
        k, v = one.split("=", 1)
        manual_cookies[k] = v
    return merge_cookies(s.cookies, manual_cookies)
