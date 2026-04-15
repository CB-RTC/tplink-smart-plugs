from __future__ import annotations


def tp_link_encrypt(plain_text: str) -> bytes:
    """Encrypt payload using TP-Link's simple XOR autokey cipher."""
    key = 171
    encrypted = bytearray()

    for byte in plain_text.encode("utf-8"):
        cipher_byte = key ^ byte
        key = cipher_byte
        encrypted.append(cipher_byte)

    return bytes(encrypted)


def tp_link_decrypt(cipher_bytes: bytes) -> str:
    """Decrypt payload returned by TP-Link devices."""
    key = 171
    decrypted = bytearray()

    for byte in cipher_bytes:
        plain_byte = key ^ byte
        key = byte
        decrypted.append(plain_byte)

    return decrypted.decode("utf-8", errors="replace")
