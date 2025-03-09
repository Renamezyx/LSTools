from app import create_app
from extensions import socketio

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="127.0.0.1", port=8080, debug=True)
