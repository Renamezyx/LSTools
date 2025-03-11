import subprocess
from dao.dao_script_storage import DaoScriptStorage

scripts = {"shutdown": "shutdown"}


def script_start(script_name: str, script_params: list = []):
    try:
        process = subprocess.Popen([scripts[script_name], *script_params], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        dao_script_storage = DaoScriptStorage()
        dao_script_storage.insert((process.pid, script_name, script_params))
        return {"code": 0, "pid": process.pid}
    except Exception as e:
        print(e)
        return {"code": -1, "error": str(e)}


def script_stop(pid: int = None, script_name: str = ""):
    res = []
    scripts_detail = []
    dao_script_storage = DaoScriptStorage()
    if pid is not None:
        scripts_detail.append({"pid": pid, "script_name": "Unknown"})
    else:
        scripts_detail = dao_script_storage.select(script_name)

    for script in scripts_detail:
        try:
            process = subprocess.Popen(
                ["taskkill", "/PID", str(script["pid"]), "/F"],  # 使用 taskkill
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # 让输出为字符串
            )
            stdout, stderr = process.communicate()  # 读取输出

            if process.returncode == 0:
                result_message = stdout.strip()
                dao_script_storage.delete(script["pid"])
            else:
                result_message = stderr.strip()  # 任务失败时返回错误信息

            res.append({"message": f"{script['script_name']}_{script['pid']}", "result": result_message})

        except Exception as e:
            res.append({"message": f"{script['script_name']}_{script['pid']}", "result": str(e)})

    return res


def script_status(script_name: str = None):
    pass


def script_custom(script: str):
    pass
