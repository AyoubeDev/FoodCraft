import json

STATUS_TEXT = {
    200: "OK",
    201: "Created",
    204: "No Content",
    400: "Bad Request",
    404: "Not Found",
    500: "Internal Server Error",
    502: "Bad Gateway",
}


class Response:
    def __init__(self, status, body=None):
        self.status = status
        self.body = body  # dict, list o None

    @property
    def reason(self):
        return STATUS_TEXT[self.status]

    def to_json(self):
        """Response -> texto JSON."""
        return "" if self.body is None else json.dumps(self.body)

    @staticmethod
    def from_json(status, text):
        """Texto JSON -> Response."""
        return Response(status, json.loads(text) if text else None)

    @staticmethod
    def error(status, message):
        return Response(status, {"error": message})
