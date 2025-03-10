from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet', path="/ws")
# socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')
