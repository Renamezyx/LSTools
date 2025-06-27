import time

from scripts.proxy_script import ProxyScript


@ProxyScript.apply_proxy_script("./scripts/get_cookies_tiktokv_script.py")
def get_battle_headers(sleep_time):
    while True:
        time.sleep(sleep_time)
        break


@ProxyScript.apply_proxy_script("./scripts/get_res_game_studio_setting.py")
def get_game_studio_setting(sleep_time):
    while True:
        time.sleep(sleep_time)
        break
