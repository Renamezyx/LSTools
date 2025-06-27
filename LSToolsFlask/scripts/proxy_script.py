import time

from config import get_project_root
from scripts.proxy_setting import ProxySetting
from scripts.mitm_proxy_manager import MitmProxyManager


class ProxyScript(object):
    @staticmethod
    def apply_proxy_script(script_path):
        def decorator_repeat(func):
            def wrapper(*args, **kwargs):
                manager = MitmProxyManager(["mitmdump", "-s", script_path, "-p", "8003"], cwd=get_project_root())
                proxy_setting = ProxySetting()
                manager.start()
                proxy_setting.set_proxy("127.0.0.1:8003")
                func(*args, **kwargs)
                manager.stop()
                proxy_setting.default_proxy()

            return wrapper

        return decorator_repeat


if __name__ == '__main__':
    @ProxyScript.apply_proxy_script("./scripts/get_cookies_tiktokv_script.py")
    def dosomething(sleep_time):
        while True:
            time.sleep(sleep_time)
            break


    dosomething(10)
