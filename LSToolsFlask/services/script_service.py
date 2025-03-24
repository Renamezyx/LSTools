import os
import subprocess

import chardet

from dao.dao_script_storage import DaoScriptStorage
from config import get_project_root


class ScriptService:
    scripts = {
        "shutdown": ["shutdown", "-s", "-t"],
        "push_script": [
            os.path.join(get_project_root(), "venv", "Scripts", "python.exe"),
            "-m", "scripts.push_stream"
        ]}

    @staticmethod
    def script_start_ws(script_name: str, user_phone: str = "", script_params: list = None):
        try:
            os.chdir(get_project_root())
            command = ScriptService.scripts[script_name]
            if not isinstance(command, list):
                command = [command]
            full_command = command[:]
            full_command.extend(script_params)
            print("cmdline: ", full_command)
            process = subprocess.Popen(full_command, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       bufsize=-1)

            dao_script_storage = DaoScriptStorage()
            dao_script_storage.insert(pid=process.pid, name=script_name, cmdline=str(full_command),
                                      user_phone=user_phone)
            try:
                for line in iter(process.stdout.readline, b''):
                    yield {"code": 0, "pid": process.pid, "out": ScriptService._safe_decode(line).strip()}
            finally:
                process.stdout.close()
                process.wait()
                dao_script_storage.delete(process.pid)
                yield {"code": 1, "pid": process.pid, "out": "进程结束"}
        except Exception as e:
            print(e)
            yield {"code": -1, "error": str(e)}

    def script_start(script_name: str, user_phone: str = "", script_params: list = None):
        try:
            os.chdir(get_project_root())
            command = ScriptService.scripts[script_name]
            if not isinstance(command, list):
                command = [command]
            full_command = command[:]
            full_command.extend(script_params)
            print("cmdline: ", full_command)
            process = subprocess.Popen(full_command, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)

            dao_script_storage = DaoScriptStorage()
            dao_script_storage.insert(pid=process.pid, name=script_name, cmdline=str(full_command),
                                      user_phone=user_phone)
            return {"code": 0, "pid": process.pid}
        except Exception as e:
            return {"code": -1, "error": str(e)}

    @staticmethod
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

    @staticmethod
    def script_status(script_name: str = None):
        pass

    @staticmethod
    def script_custom(script: str):
        pass

    @staticmethod
    def _safe_decode(byte_str):
        """自动检测编码并解码，兼容中文、英文、表情符号"""
        try:
            # 使用 chardet 检测编码
            detected = chardet.detect(byte_str)
            encoding = detected["encoding"] or "utf-8"
            return byte_str.decode(encoding, errors="ignore")
        except UnicodeDecodeError:
            return byte_str.decode("utf-8", errors="ignore")


if __name__ == '__main__':
    s = ScriptService.script_start("shutdown", ["1800"])
    for i in s:
        print(i)
