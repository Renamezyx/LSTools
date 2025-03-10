import subprocess
from dao.dao_script_storage import DaoScriptStorage
scripts = {"shutdown": "shutdown"}


def script_start(script_name: str, script_params: list = []):
    try:
        process = subprocess.Popen([scripts[script_name], *script_params], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        dao_script_storage = DaoScriptStorage()
        dao_script_storage.insert((process.pid, script_name, script_params))
        return process.pid
    except Exception as e:
        print(e)
        return -1


def script_stop(pid: int = None, script_name: str = None, ):
    pass


def script_status(script_name: str = None):
    pass


def script_custom(script: str):
    pass
