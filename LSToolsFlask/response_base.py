import time


class Response(object):
    def __init__(self, code: int = 200, message: str = '', data: dict = {}):
        self.start_time = None
        self.code = code
        self.message = message
        self.data = data

    @property
    def timestamp(self) -> int:
        return int(round(time.time() * 1000))

    @property
    def dict(self) -> dict:
        return {"code": self.code, "message": self.message, "data": self.data, "timestamp": self.timestamp}

    def start(self):
        self.start_time = int(round(time.time() * 1000))

    @property
    def run_speed(self) -> dict:
        return {"code": self.code, "message": self.message, "data": self.data, "timestamp": self.timestamp, "run_speed"
        : '{0}ms'.format(self.timestamp - self.start_time)}


response = Response()

if __name__ == '__main__':
    res = Response()
    print(res.dict)
    time.sleep(2)
    print(res.dict)
