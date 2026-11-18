"""Generate local TLS certificates. Install cryptography to run this once."""
import datetime
import ipaddress
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

CERT_DIR = Path(__file__).resolve().parents[1] / "certs"
NOW = datetime.datetime.now(datetime.timezone.utc)


def make_certificate(name, key, issuer, issuer_key, is_ca=False):
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, name)])
    signing_key = issuer_key or key
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer.subject if issuer else subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(NOW - datetime.timedelta(minutes=5))
        .not_valid_after(NOW + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(signing_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=0 if is_ca else None),
            critical=True,
        )
    )
    if not is_ca:
        names = [
            x509.DNSName("localhost"),
            x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
        ]
        builder = builder.add_extension(
            x509.SubjectAlternativeName(names),
            critical=False,
        )
        builder = builder.add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
    else:
        builder = builder.add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=None,
                decipher_only=None,
            ),
            critical=True,
        )
    return builder.sign(signing_key, hashes.SHA256())


def save_key(name, key):
    path = CERT_DIR / f"{name}-key.pem"
    path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )


def save_certificate(name, certificate):
    path = CERT_DIR / f"{name}-cert.pem"
    path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))


def main():
    CERT_DIR.mkdir(exist_ok=True)

    ca_key = ec.generate_private_key(ec.SECP256R1())
    ca_certificate = make_certificate("FoodCraft CA", ca_key, None, None, is_ca=True)
    save_certificate("ca", ca_certificate)

    for service in ("api", "backend"):
        key = ec.generate_private_key(ec.SECP256R1())
        certificate = make_certificate(service, key, ca_certificate, ca_key)
        save_key(service, key)
        save_certificate(service, certificate)

    print(f"TLS certificates generated in {CERT_DIR}")


if __name__ == "__main__":
    main()
