from __future__ import annotations

import json
import hashlib
from copy import deepcopy
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


BASE_DIR = Path(__file__).resolve().parent
KEYS_DIR = BASE_DIR / "keys"
DATA_DIR = BASE_DIR / "data"

PRIVATE_KEY_PATH = KEYS_DIR / "private_key.pem"
PUBLIC_KEY_PATH = KEYS_DIR / "public_key.pem"

ORIGINAL_TRANSACTION_PATH = DATA_DIR / "transaccion_original.json"
ALTERED_TRANSACTION_PATH = DATA_DIR / "transaccion_alterada.json"
SIGNATURE_PATH = DATA_DIR / "firma_transaccion.bin"


def ensure_directories() -> None:
    """Crea las carpetas necesarias si no existen."""
    KEYS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_json_pretty(path: Path, data: dict[str, Any]) -> None:
    """Guarda JSON legible para revisarlo fácilmente."""
    path.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def canonical_json_bytes(data: dict[str, Any]) -> bytes:
    """
    Convierte el JSON a una representación canónica para que
    el hash y la firma sean consistentes.
    """
    canonical = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )
    return canonical.encode("utf-8")


def generate_keys_if_missing() -> None:
    """Genera un par de claves RSA si todavía no existen."""
    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        print("Las claves RSA ya existen. Se reutilizarán.")
        return

    print("Generando claves RSA de 2048 bits...")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    PRIVATE_KEY_PATH.write_bytes(private_pem)
    PUBLIC_KEY_PATH.write_bytes(public_pem)

    print(f"Clave privada guardada en: {PRIVATE_KEY_PATH}")
    print(f"Clave pública guardada en:  {PUBLIC_KEY_PATH}")


def load_private_key():
    """Carga la clave privada desde el archivo PEM."""
    return serialization.load_pem_private_key(
        PRIVATE_KEY_PATH.read_bytes(),
        password=None
    )


def load_public_key():
    """Carga la clave pública desde el archivo PEM."""
    return serialization.load_pem_public_key(
        PUBLIC_KEY_PATH.read_bytes()
    )


def build_sample_transaction() -> dict[str, Any]:
    """Crea una transacción bancaria de ejemplo para la demo."""
    return {
        "bank": "State Safe Bank",
        "transaction_id": "TXN-2026-0001",
        "customer": {
            "full_name": "Laura Gómez",
            "document_id": "1020304050",
            "account_number": "458912340078"
        },
        "transaction": {
            "type": "TRANSFERENCIA",
            "amount": 1850000.75,
            "currency": "COP",
            "timestamp": "2026-04-17T14:25:00",
            "destination_account": "998877665544"
        },
        "status": "APROBADA"
    }


def calculate_sha256(data_bytes: bytes) -> str:
    """Calcula el hash SHA-256 en formato hexadecimal."""
    return hashlib.sha256(data_bytes).hexdigest()


def sign_data(private_key, data_bytes: bytes) -> bytes:
    """Firma digitalmente los datos usando RSA + PSS + SHA-256."""
    signature = private_key.sign(
        data_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verify_signature(public_key, data_bytes: bytes, signature: bytes) -> bool:
    """Verifica la firma digital. Devuelve True si es válida, False si no."""
    try:
        public_key.verify(
            signature,
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


def print_separator() -> None:
    print("\n" + "=" * 80 + "\n")


def main() -> None:
    ensure_directories()
    generate_keys_if_missing()

    private_key = load_private_key()
    public_key = load_public_key()

    # 1) Crear y guardar la transacción original
    original_transaction = build_sample_transaction()
    save_json_pretty(ORIGINAL_TRANSACTION_PATH, original_transaction)

    # 2) Convertir a JSON canónico y calcular hash
    original_bytes = canonical_json_bytes(original_transaction)
    original_hash = calculate_sha256(original_bytes)

    # 3) Firmar la transacción
    signature = sign_data(private_key, original_bytes)
    SIGNATURE_PATH.write_bytes(signature)

    # 4) Verificar la firma de la transacción original
    original_is_valid = verify_signature(public_key, original_bytes, signature)

    print_separator()
    print("TRANSACCIÓN ORIGINAL")
    print_separator()
    print(f"Archivo JSON:       {ORIGINAL_TRANSACTION_PATH}")
    print(f"Hash SHA-256:       {original_hash}")
    print(f"Archivo de firma:   {SIGNATURE_PATH}")
    print(f"Firma válida:       {'SÍ' if original_is_valid else 'NO'}")

    # 5) Alterar una copia de la transacción
    altered_transaction = deepcopy(original_transaction)
    altered_transaction["transaction"]["amount"] = 9850000.99
    altered_transaction["status"] = "MODIFICADA"

    save_json_pretty(ALTERED_TRANSACTION_PATH, altered_transaction)

    # 6) Calcular hash de la transacción alterada
    altered_bytes = canonical_json_bytes(altered_transaction)
    altered_hash = calculate_sha256(altered_bytes)

    # 7) Verificar la transacción alterada con la firma original
    altered_is_valid = verify_signature(public_key, altered_bytes, signature)

    print_separator()
    print("TRANSACCIÓN ALTERADA")
    print_separator()
    print(f"Archivo JSON:       {ALTERED_TRANSACTION_PATH}")
    print(f"Hash SHA-256:       {altered_hash}")
    print(f"Firma válida:       {'SÍ' if altered_is_valid else 'NO'}")

    print_separator()
    print("COMPARACIÓN FINAL")
    print_separator()
    print(f"¿El hash cambió?:   {'SÍ' if original_hash != altered_hash else 'NO'}")
    print(
        "¿Se detectó alteración?: "
        f"{'SÍ, la verificación falló' if not altered_is_valid else 'NO'}"
    )

    print_separator()
    print("RESUMEN")
    print_separator()
    print("1. La transacción original fue firmada correctamente con RSA.")
    print("2. La verificación de la transacción original fue exitosa.")
    print("3. Al modificar el monto y el estado, cambió el hash SHA-256.")
    print("4. La firma original ya no fue válida sobre los datos alterados.")
    print("5. Esto demuestra cómo la criptografía ayuda a garantizar la integridad de los datos.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print_separator()
        print("Ocurrió un error durante la ejecución del script.")
        print(f"Detalle: {error}")
        raise