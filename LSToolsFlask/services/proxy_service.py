import time

from scripts.proxy_script import ProxyScript


@ProxyScript.apply_proxy_script("./scripts/get_cookies_tiktokv_script.py")
def get_battle_headers(sleep_time):
    while True:
        time.sleep(sleep_time)
        break
