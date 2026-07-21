"""
Encryption — AES-256-GCM encrypt/decrypt for private playlists.

Users can encrypt their private playlists using the Colab notebook,
then drop the .enc files in the input/ folder. The engine will decrypt
them if the key is provided.
"""

import os
from .utils import setup_logging

logger = setup_logging("engine.encryption")


def encrypt_playlist(input_file: str, output_file: str, key_hex: str) -> str | None:
    """Encrypt a plaintext M3U file using AES-256-GCM.

    Args:
        input_file: Path to plaintext .m3u file
        output_file: Path for output .enc file
        key_hex: 64-character hex string (32 bytes) for AES-256

    Returns:
        Output file path on success, None on failure
    """
    try:
        from Crypto.Cipher import AES
        from Crypto.Random import get_random_bytes
    except ImportError:
        logger.error("Install pycryptodome: pip install pycryptodome")
        return None

    # Validate key
    key = bytes.fromhex(key_hex)
    if len(key) != 32:
        logger.error("Key must be exactly 32 bytes (64 hex characters)")
        return None

    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return None

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Generate random 12-byte IV for GCM
    iv = get_random_bytes(12)

    # Encrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # Write: [IV: 12 bytes] [Tag: 16 bytes] [Ciphertext]
    with open(output_file, 'wb') as f:
        f.write(iv)
        f.write(tag)
        f.write(ciphertext)

    logger.info(f"Encrypted: {input_file} → {output_file}")
    return output_file


def decrypt_playlist(input_file: str, output_file: str, key_hex: str) -> str | None:
    """Decrypt an AES-256-GCM encrypted playlist file.

    Args:
        input_file: Path to .enc file
        output_file: Path for output .m3u file
        key_hex: 64-character hex string (32 bytes) for AES-256

    Returns:
        Output file path on success, None on failure
    """
    try:
        from Crypto.Cipher import AES
    except ImportError:
        logger.error("Install pycryptodome: pip install pycryptodome")
        return None

    # Validate key
    key = bytes.fromhex(key_hex)
    if len(key) != 32:
        logger.error("Key must be exactly 32 bytes (64 hex characters)")
        return None

    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return None

    with open(input_file, 'rb') as f:
        iv = f.read(12)
        tag = f.read(16)
        ciphertext = f.read()

    # Decrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    with open(output_file, 'wb') as f:
        f.write(plaintext)

    logger.info(f"Decrypted: {input_file} → {output_file}")
    return output_file


def generate_key() -> str:
    """Generate a random 256-bit key as hex string."""
    try:
        from Crypto.Random import get_random_bytes
        key = get_random_bytes(32)
        return key.hex()
    except ImportError:
        import secrets
        return secrets.token_hex(32)