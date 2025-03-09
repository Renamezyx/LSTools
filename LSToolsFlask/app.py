from flask import Flask
from extensions import socketio
from routes import api
from routes import ws_routes  # 确保 WebSocket 事件已注册


def create_app():
    app = Flask(__name__)


    # 初始化 API
    api.init_app(app)

    # 初始化 WebSocket
    socketio.init_app(app)

    return app


