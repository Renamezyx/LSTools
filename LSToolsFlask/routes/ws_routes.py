from flask_socketio import emit
from extensions import socketio
from services.trends_stats_service import get_trends_stats

server_response = {
    "code": 0,
    "type": "",
    "data": {}
}


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("server_response", server_response)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("message")
def handle_message(message):
    # message = {
    #     "func": "get_trends_stats",
    #     "start_time": 1741449355
    # }
    print(f"Received message: {message}")
    if isinstance(message, dict) and "func" in message:
        func_name = message.get("func")
        server_response = {
            "code": 0,
            "data": {}
        }

        match func_name:
            case "get_trends_stats":
                start_time = message.get("start_time", None)
                server_response["type"] = "get_trends_stats"
                server_response["data"] = get_trends_stats(start_time)
            case _:
                # 如果 func_name 不匹配，处理未定义的情况
                server_response["code"] = 1
                server_response["data"] = "Invalid function"

        emit("server_response", server_response)
    else:
        # 如果 message 不符合预期格式，返回错误
        emit("server_response", {
            "code": 1,
            "data": "Invalid message format"
        })


@socketio.on("custom_event")
def handle_custom_event(data):
    print(f"Received custom event with data: {data}")
    emit("server_response", server_response)
