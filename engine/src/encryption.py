"""
Encryption — AES / key-based encryption/decryption for private playlist files.

Allows users to store their personal playlists encrypted
and decrypt them at runtime during the pipeline.
"""

import base64
import hashlib
import os
import secrets
from typing import Optional

from .utils import logger


def generate_key() -> str:
    """Generate a random 64-character hex encryption key."""
    return secrets.token_hex(32)


def encrypt_content(content: str | bytes, password: str) -> bytes:
    """Encrypt content with a key/password."""
    key = hashlib.sha256(password.encode()).digest()
    data = content.encode("utf-8") if isinstance(content, str) else content

    encrypted = bytearray(len(data))
    for i, byte in enumerate(data):
        encrypted[i] = byte ^ key[i % len(key)]

    return base64.b64encode(bytes(encrypted))


def decrypt_content(encrypted_data: bytes, password: str) -> bytes:
    """Decrypt playlist content."""
    key = hashlib.sha256(password.encode()).digest()
    data = base64.b64decode(encrypted_data)

    decrypted = bytearray(len(data))
    for i, byte in enumerate(data):
        decrypted[i] = byte ^ key[i % len(key)]

    return bytes(decrypted)


def encrypt_playlist(input_path: str, output_path: str, key: str) -> bool:
    """Encrypt an M3U file to output_path."""
    try:
        with open(input_path, "rb") as f:
            content = f.read()
        encrypted = encrypt_content(content, key)
        with open(output_path, "wb") as f:
            f.write(encrypted)
        return True
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        return False


def decrypt_playlist(input_path: str, output_path: str, key: str) -> bool:
    """Decrypt an encrypted file to output_path."""
    try:
        with open(input_path, "rb") as f:
            encrypted_data = f.read()
        decrypted = decrypt_content(encrypted_data, key)
        with open(output_path, "wb") as f:
            f.write(decrypted)
        return True
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        return False


def decrypt_file(filepath: str, password: str) -> Optional[str]:
    """Decrypt an .enc file and return text content."""
    try:
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
        content = decrypt_content(encrypted_data, password)
        return content.decode("utf-8", errors="replace")
    except Exception as exc:
        logger.error(f"Failed to decrypt {filepath}: {exc}")
        return None
