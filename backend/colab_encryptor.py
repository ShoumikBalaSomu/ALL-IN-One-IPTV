"""
ALL-IN-One-IPTV Google Colab Encryptor (AES-256-GCM)

Instructions for Colab:
1. !pip install pycryptodome
2. Set your ENV_PLAYLIST_KEY (Must be exactly 32 bytes for AES-256)
3. Run this script pointing to your plaintext .m3u
4. Download the generated .enc file and push it to the GitHub input/ folder.
"""

import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_playlist(input_file: str, output_file: str, key_hex: str):
    # Ensure key is 32 bytes (64 hex characters)
    key = bytes.fromhex(key_hex)
    if len(key) != 32:
        raise ValueError("Key must be exactly 32 bytes (64 hex characters) for AES-256")

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Generate random 12-byte Initialization Vector (IV) for GCM
    iv = get_random_bytes(12)
    
    # Initialize AES-GCM cipher
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # Output structure: [IV (12 bytes)] + [Tag (16 bytes)] + [Ciphertext]
    with open(output_file, 'wb') as f:
        f.write(iv)
        f.write(tag)
        f.write(ciphertext)
        
    print(f"Successfully encrypted {input_file} -> {output_file}")
    
    # Memory Wipe (Basic precaution in Python)
    plaintext = bytearray(len(plaintext))
    del plaintext

if __name__ == "__main__":
    # Example usage:
    # KEY = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    # encrypt_playlist("my_private_streams.m3u", "my_private_streams.enc", KEY)
    pass
