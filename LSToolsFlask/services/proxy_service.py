import time

from scripts.script import SCRIPT


@SCRIPT.apply_proxy_script("./scripts/get_cookies_baidu_script.py")
def get_battle_headers(sleep_time):
    while True:
        time.sleep(sleep_time)
        break

