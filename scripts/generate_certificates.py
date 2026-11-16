"""Genera la CA y los certificados de servidor y cliente en certificates/.

Necesita `pip install cryptography` (solo para generar; los servidores usan `ssl`).
Si TLS_KEY_PASSWORD esta definida, las claves se guardan cifradas con ella.
Uso: python scripts/generate_certificates.py
"""
import datetime
import ipaddress
import os
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

CERT_DIR = Path(__file__).resolve().parents[1] / "certificates"
PASSWORD = os.getenv("TLS_KEY_PASSWORD")
NOW = datetime.datetime.now(datetime.timezone.utc)


def new_certificate(common_name, issuer_name, issuer_key, extensions):
    key = ec.generate_private_key(ec.SECP256R1())
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer_name or subject)  # la CA se firma a si misma
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(NOW - datetime.timedelta(minutes=5))
        .not_valid_after(NOW + datetime.timedelta(days=365))
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
    )
    for extension, critical in extensions:
        builder = builder.add_extension(extension, critical)
    certificate = builder.sign(issuer_key or key, hashes.SHA256())
    return key, certificate


def save(name, key, certificate):
    if PASSWORD:
        encryption = serialization.BestAvailableEncryption(PASSWORD.encode())
    else:
        encryption = serialization.NoEncryption()
    (CERT_DIR / f"{name}.key").write_bytes(key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, encryption
    ))
    (CERT_DIR / f"{name}.crt").write_bytes(certificate.public_bytes(serialization.Encoding.PEM))


def leaf_extensions(ca_key, usage, alt_names=None):
    extensions = [
        (x509.BasicConstraints(ca=False, path_length=None), True),
        (x509.KeyUsage(digital_signature=True, content_commitment=False, key_encipherment=False,
                       data_encipherment=False, key_agreement=True, key_cert_sign=False,
                       crl_sign=False, encipher_only=False, decipher_only=False), True),
        (x509.ExtendedKeyUsage([usage]), False),
        (x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), False),
    ]
    if alt_names:
        extensions.append((x509.SubjectAlternativeName(alt_names), False))
    return extensions


def main():
    CERT_DIR.mkdir(exist_ok=True)

    ca_extensions = [
        (x509.BasicConstraints(ca=True, path_length=0), True),
        (x509.KeyUsage(digital_signature=True, content_commitment=False, key_encipherment=False,
                       data_encipherment=False, key_agreement=False, key_cert_sign=True,
                       crl_sign=True, encipher_only=False, decipher_only=False), True),
    ]
    ca_key, ca_certificate = new_certificate("FoodCraft CA", None, None, ca_extensions)
    save("ca", ca_key, ca_certificate)

    server_names = [x509.DNSName("localhost"), x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]
    server_key, server_certificate = new_certificate(
        "FoodCraft Server", ca_certificate.subject, ca_key,
        leaf_extensions(ca_key, ExtendedKeyUsageOID.SERVER_AUTH, server_names),
    )
    save("server", server_key, server_certificate)

    client_key, client_certificate = new_certificate(
        "FoodCraft Client", ca_certificate.subject, ca_key,
        leaf_extensions(ca_key, ExtendedKeyUsageOID.CLIENT_AUTH),
    )
    save("client", client_key, client_certificate)
    print(f"Certificados generados en {CERT_DIR}")


if __name__ == "__main__":
    main()
