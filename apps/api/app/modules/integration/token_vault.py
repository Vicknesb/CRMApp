"""
Encrypted token vault for OAuth credentials.
Uses AES-256-GCM via the cryptography library.
Key is derived from SECRET_KEY in settings.
"""
import base64
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import settings


def _key() -> bytes:
    raw = settings.secret_key.encode()
    # Pad/truncate to 32 bytes for AES-256
    return (raw * 4)[:32]


def encrypt_token(data: dict) -> str:
    key = _key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    plaintext = json.dumps(data).encode()
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return base64.urlsafe_b64encode(nonce + ciphertext).decode()


def decrypt_token(encrypted: str) -> dict:
    key = _key()
    aesgcm = AESGCM(key)
    raw = base64.urlsafe_b64decode(encrypted.encode())
    nonce, ciphertext = raw[:12], raw[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(plaintext)
