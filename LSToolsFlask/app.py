import multiprocessing

from flask import Flask
from flask_cors import CORS

from extensions import socketio
from routes import api
from routes import ws_routes  # 确保 WebSocket 事件已注册


def create_app():
    app = Flask(__name__)

    # 初始化 API
    api.init_app(app)

    # 初始化 WebSocket
    socketio.init_app(app, cors_allowed_origins="*")  # 允许 WebSocket 跨域

    # 允许 CORS（推荐配置更精确的规则）
    CORS(app, resources={r"/*": {"origins": "*"}})

    return app
