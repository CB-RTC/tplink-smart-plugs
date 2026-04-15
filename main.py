from __future__ import annotations

import argparse
import json
import socket
from typing import Any


DEFAULT_IPS = ["192.168.0.193", "192.168.0.195", "192.168.0.196"]
TPLINK_PORT = 9999
SOCKET_TIMEOUT_SECONDS = 5


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


def send_tplink_command(ip: str, command: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps(command, separators=(",", ":"))
    encrypted_payload = tp_link_encrypt(payload)
    message = len(encrypted_payload).to_bytes(4, byteorder="big") + encrypted_payload

    with socket.create_connection((ip, TPLINK_PORT), timeout=SOCKET_TIMEOUT_SECONDS) as sock:
        sock.sendall(message)
        response = sock.recv(4096)

    if len(response) >= 4:
        response = response[4:]

    decoded = tp_link_decrypt(response)
    return json.loads(decoded)


def set_plug_state(ip: str, state: bool) -> None:
    command = {"system": {"set_relay_state": {"state": int(state)}}}
    result = send_tplink_command(ip, command)
    err_code = result.get("system", {}).get("set_relay_state", {}).get("err_code")

    if err_code == 0:
        print(f"{ip}: {'ON' if state else 'OFF'}")
    else:
        print(f"{ip}: device returned err_code={err_code} | response={result}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Control TP-Link smart plugs over raw TCP socket.")
    parser.add_argument("action", choices=["on", "off"], help="Set relay state on selected plugs.")
    parser.add_argument(
        "--ips",
        nargs="+",
        default=DEFAULT_IPS,
        help="One or more plug IP addresses (default: 192.168.0.193 192.168.0.195 192.168.0.196).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_state = args.action == "on"

    for ip in args.ips:
        try:
            set_plug_state(ip, target_state)
        except (socket.timeout, ConnectionError, OSError) as exc:
            print(f"{ip}: connection failed ({exc})")
        except json.JSONDecodeError as exc:
            print(f"{ip}: invalid JSON response ({exc})")


if __name__ == "__main__":
    main()
