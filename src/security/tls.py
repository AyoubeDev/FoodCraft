import os
import ssl
from pathlib import Path

# Certificados de cada pieza (los genera scripts/generate_certificates.py)
CERT_DIR = Path(__file__).resolve().parents[2] / "certificates"
KEY_PASSWORD = os.getenv("TLS_KEY_PASSWORD")  # solo si las claves estan cifradas


def server_context() -> ssl.SSLContext:
    """Contexto para quien escucha: TLS 1.3 y exige certificado al cliente (mTLS)."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain(CERT_DIR / "server.crt", CERT_DIR / "server.key", KEY_PASSWORD)
    context.load_verify_locations(CERT_DIR / "ca.crt")  # CA que firmo los certificados de cliente
    context.verify_mode = ssl.CERT_REQUIRED
    return context


def client_context() -> ssl.SSLContext:
    """Contexto para quien se conecta: TLS 1.3, comprueba al servidor y presenta su certificado."""
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CERT_DIR / "ca.crt")
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain(CERT_DIR / "client.crt", CERT_DIR / "client.key", KEY_PASSWORD)
    return context


def wrap_connection(context: ssl.SSLContext, raw_socket):
    """Hace el handshake TLS de una conexion aceptada. Si falla, la cierra y devuelve None."""
    raw_socket.settimeout(10)  # un cliente que no completa el handshake no se queda colgado
    try:
        return context.wrap_socket(raw_socket, server_side=True)
    except OSError:  # ssl.SSLError y los cortes de conexion
        raw_socket.close()
        return None
