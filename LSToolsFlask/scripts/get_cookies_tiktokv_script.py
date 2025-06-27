import os.path
import sys

from urllib.parse import urlparse
from mitmproxy import http
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)  # 保证优先级
from config import get_project_root
from utils.json_file_handler import JSONFileHandler


def request(flow: http.HTTPFlow):
    # 获取完整的URL信息
    if "battle/invite/" in flow.request.url:
        url_parsed = urlparse(flow.request.url)
        key = "tiktokv"
        value = dict(flow.request.headers)
        value["Host"] = flow.request.host_header
        JSONFileHandler.update_json(os.path.join(get_project_root(), "headers.json"), key, value)
