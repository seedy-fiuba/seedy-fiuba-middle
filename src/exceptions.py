

class MiddleException(Exception):
    def __init__(self, status: int, detail: dict):
        self.status = status,
        self.detail = detail

