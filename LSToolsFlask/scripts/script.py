import subprocess
import time

from proxy import Proxy


class MitmProxyManager:
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def start(self):
        try:
            self.process = subprocess.Popen(self.cmd)
            print("mitmdump started successfully.")
        except Exception as e:
            print("Error starting mitmdump:", e)

    def stop(self):
        if self.process:
            self.process.terminate()
            print("mitmdump stopped.")
        else:
            print("mitmdump is not running.")

    def __del__(self):
        self.stop()


class SCRIPT(object):
    @staticmethod
    def apply_proxy_script(script_path):
        def decorator_repeat(func):
            def wrapper(*args, **kwargs):
                manager = MitmProxyManager(["mitmdump", "-s", script_path, "-p", "8002"])
                proxy = Proxy()
                manager.start()
                proxy.set_proxy("127.0.0.1:8002")
                func(*args, **kwargs)
                manager.stop()
                proxy.default_proxy()

            return wrapper

        return decorator_repeat


if __name__ == '__main__':
    @SCRIPT.apply_proxy_script("./scripts/get_cookies_baidu_script.py")
    def dosomething(sleep_time):
        while True:
            time.sleep(sleep_time)
            break


    dosomething(10)
