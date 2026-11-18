import socket
import ssl
from pathlib import Path

CERT_DIR = Path(__file__).resolve().parents[2] / "certs"
CA_CERT = CERT_DIR / "ca-cert.pem"


def server_context(service: str) -> ssl.SSLContext:
    """Create a TLS 1.3 context for the API or backend server."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain(
        CERT_DIR / f"{service}-cert.pem",
        CERT_DIR / f"{service}-key.pem",
    )
    return context


def client_context():
    """Create a TLS 1.3 context that verifies the server certificate."""
    context = ssl.create_default_context(cafile=CA_CERT)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    return context


def wrap_connection(context, raw_socket):
    """Complete TLS for an accepted connection; close it if the handshake fails."""
    raw_socket.settimeout(10)
    try:
        return context.wrap_socket(raw_socket, server_side=True)
    except OSError:
        raw_socket.close()
        return None
