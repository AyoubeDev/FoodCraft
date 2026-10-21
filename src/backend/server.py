import json
import os
import socket
import threading

from backend.dispatcher import dispatch
from backend.responses import ResponseBuilder

# Solo acepta conexiones de la propia maquina. Para que la API este en otro equipo: BACKEND_HOST=0.0.0.0
HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
PORT = int(os.getenv("BACKEND_PORT", "9000"))


def handle(api):
    """Atiende UNA orden de la API: leer, ejecutar, responder y cerrar."""
    try:
        line = b""
        while not line.endswith(b"\n"):  # la orden es una linea JSON
            line += api.recv(1024)

        response = dispatch(json.loads(line))
    except Exception as error:
        response = ResponseBuilder.server_error(str(error))

    # default=str convierte fechas y decimales a texto
    reply = json.dumps({"status": response.status, "body": response.body}, default=str)
    api.sendall(reply.encode("utf-8") + b"\n")
    api.close()


def run():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Backend escuchando en {HOST}:{PORT}")

    while True:
        api, _address = server.accept()
        threading.Thread(target=handle, args=(api,)).start()


if __name__ == "__main__":
    run()
