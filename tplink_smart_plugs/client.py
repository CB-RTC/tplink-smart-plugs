from __future__ import annotations

import json
import socket
from typing import Any

from tplink_smart_plugs import SOCKET_TIMEOUT_SECONDS, TPLINK_PORT
from tplink_smart_plugs.crypto import tp_link_decrypt, tp_link_encrypt


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
