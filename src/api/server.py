import socket

from api import Request, Response, find_route
from api.backend_client import send_order
from api.http_message import build_response, read_request

HOST = "0.0.0.0"  # 0.0.0.0 = acepta conexiones de otros equipos de la red
PORT = 8000


def handle(client):
    """Atiende UNA peticion del cliente: leer, reenviar al backend, responder y cerrar."""
    try:
        request = read_request(client)
        route = find_route(request.method, request.path)

        if route is None:
            response = Response.error(404, "Route not found")
        else:
            name, params = route
            table = name.split(".")[0]
            body = Request.from_json(table, request.body).data  # solo los campos de la tabla
            response = send_order(name, params, request.query, body)
    except ValueError as error:  # JSON roto
        response = Response.error(400, str(error))
    except Exception as error:
        response = Response.error(500, str(error))

    client.sendall(build_response(response))
    client.close()


def run():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"API escuchando en {HOST}:{PORT}")

    while True:
        client, _address = server.accept()
        handle(client)  # un cliente a la vez; sin hilos por ahora


if __name__ == "__main__":
    run()
