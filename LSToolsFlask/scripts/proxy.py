import time
import winreg


class Proxy(object):
    def __init__(self):
        self.o_proxy_server = self.get_proxy

    @property
    def get_proxy(self):
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        internet_settings_key = winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
        proxy_enable, _ = winreg.QueryValueEx(internet_settings_key, 'ProxyEnable')
        if proxy_enable == 1:
            proxy_server, _ = winreg.QueryValueEx(internet_settings_key, 'ProxyServer')
            return proxy_server
        else:
            return None

    def set_proxy(self, proxy_server):
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        internet_settings_key = winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                               0, winreg.KEY_WRITE)
        if proxy_server is None:
            winreg.SetValueEx(internet_settings_key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
        else:
            winreg.SetValueEx(internet_settings_key, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(internet_settings_key, 'ProxyServer', 0, winreg.REG_SZ, proxy_server)
        winreg.CloseKey(internet_settings_key)

    def default_proxy(self):
        print(self.o_proxy_server)
        self.set_proxy(self.o_proxy_server)


if __name__ == '__main__':
    proxy = Proxy()
    proxy.set_proxy("127.0.0.1:8002")
    time.sleep(20)
    proxy.default_proxy()
