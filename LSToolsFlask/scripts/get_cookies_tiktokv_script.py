import os.path
import sys

from urllib.parse import urlparse
from mitmproxy import http

from config import get_project_root
from utils.json_file_handler import JSONFileHandler

# def get_project_root():
#     # 获取根目录 不受运行目录影响
#     current_dir = os.path.abspath(__file__)
#     while not os.path.exists(os.path.join(current_dir, '.project_root')):
#         current_dir = os.path.dirname(current_dir)
#     return current_dir


sys.path.append(os.path.join(get_project_root()))



def request(flow: http.HTTPFlow):
    # 获取完整的URL信息
    if "battle/invite/" in flow.request.url:
        url_parsed = urlparse(flow.request.url)
        key = "tiktokv"
        value = dict(flow.request.headers)
        value["Host"] = flow.request.host_header
        JSONFileHandler.update_json(os.path.join(get_project_root(), "headers.json"), key, value)
