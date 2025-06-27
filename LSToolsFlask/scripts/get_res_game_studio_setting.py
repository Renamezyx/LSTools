import os
import sys

from mitmproxy import http

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)  # 保证优先级
from config import get_project_root
from utils.json_file_handler import JSONFileHandler


def response(flow: http.HTTPFlow):
    if "/game/studio/setting/" in flow.request.url:
        try:
            resp_body = flow.response.json()
        except ValueError:
            # 防止响应不是合法 JSON
            print("响应不是 JSON 格式，跳过")
            return

        key = "setting"
        data_to_save = resp_body

        file_path = os.path.join(get_project_root(), "game_studio_setting.json")

        # 创建空 JSON 文件（如果不存在）
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('{}')  # 写入空 JSON 对象，防止 JSONDecodeError

        # 更新 JSON 文件
        JSONFileHandler.update_json(file_path, key, data_to_save)
