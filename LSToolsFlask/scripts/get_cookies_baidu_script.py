import os.path
from urllib.parse import urlparse

from mitmproxy import http
from common.logger_base import logger
from utils.json_file_handler import JSONFileHandler
from config import get_project_root


def request(flow: http.HTTPFlow):
    # 获取完整的URL信息
    if "www.baidu.com" in flow.request.url:
        url_parsed = urlparse(flow.request.url)
        key = "baidu"
        value = dict(flow.request.headers)
        logger.info(f'{key}: {value}')
        JSONFileHandler.update_json(os.path.join(get_project_root(), "headers.json"), key, value)
