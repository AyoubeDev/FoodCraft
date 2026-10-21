import json
import os
import socket

from api.responses import Response

# Donde esta el backend
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "9000"))


def send_order(name, params, query, body):
    """Manda una orden al backend (un socket nuevo por orden) y devuelve su Response."""
    order = {"name": name, "params": params, "query": query, "body": body}

    try:
        with socket.create_connection((BACKEND_HOST, BACKEND_PORT), timeout=10) as backend:
            backend.sendall(json.dumps(order).encode("utf-8") + b"\n")

            line = b""
            while not line.endswith(b"\n"):
                line += backend.recv(1024)
    except OSError:
        return Response.error(502, "Backend not available")

    reply = json.loads(line)
    return Response(reply["status"], reply["body"])
