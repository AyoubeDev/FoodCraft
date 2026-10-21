from dataclasses import dataclass


@dataclass
class HttpRequest:
    method: str
    path: str
    query: dict
    body: str


def read_request(sock) -> HttpRequest:
    """Lee del socket una peticion HTTP y la convierte en un HttpRequest."""
    # 1. Leer hasta la linea vacia que separa cabeceras y cuerpo
    data = b""
    while b"\r\n\r\n" not in data:
        data += sock.recv(1024)

    head, _, body = data.partition(b"\r\n\r\n")
    lines = head.decode("utf-8").split("\r\n")

    # 2. Primera linea: "POST /recipes?title=pasta HTTP/1.1"
    method, target, _ = lines[0].split(" ")
    path, _, query_text = target.partition("?")

    query = {}
    if query_text:
        for pair in query_text.split("&"):
            key, _, value = pair.partition("=")
            query[key] = value

    # 3. Buscar Content-Length y leer exactamente esos bytes de cuerpo
    length = 0
    for line in lines[1:]:
        if line.lower().startswith("content-length:"):
            length = int(line.split(":")[1])

    while len(body) < length:
        body += sock.recv(1024)

    return HttpRequest(method, path, query, body.decode("utf-8"))


def build_response(response) -> bytes:
    """Convierte una Response en los bytes HTTP que se envian por el socket."""
    body = response.to_json().encode("utf-8")

    text = f"HTTP/1.1 {response.status} {response.reason}\r\n"
    text += "Content-Type: application/json\r\n"
    text += f"Content-Length: {len(body)}\r\n"  # bytes, no caracteres
    text += "\r\n"

    return text.encode("utf-8") + body
