from __future__ import annotations

import argparse
import json
import socket

from tplink_smart_plugs import DEFAULT_ADDRESS_FILE
from tplink_smart_plugs.config import load_addresses
from tplink_smart_plugs.control import set_plug_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Control TP-Link smart plugs over raw TCP socket.")
    parser.add_argument("action", choices=["on", "off"], help="Set relay state on selected plugs.")
    parser.add_argument("--address", nargs="+", help="One or more plug IP addresses.")
    parser.add_argument(
        "--address-file",
        default=DEFAULT_ADDRESS_FILE,
        help="Path to file with plug IPs, one per line (default: ips.txt).",
    )
    return parser.parse_args()


def resolve_target_ips(args: argparse.Namespace) -> list[str]:
    if args.address:
        return args.address

    return load_addresses(args.address_file)


def order_66() -> None:
    args = parse_args()
    target_state = args.action == "on"

    try:
        ips = resolve_target_ips(args)
    except (FileNotFoundError, ValueError) as exc:
        print(exc)
        return

    for ip in ips:
        try:
            set_plug_state(ip, target_state)
        except (socket.timeout, ConnectionError, OSError) as exc:
            print(f"{ip}: connection failed ({exc})")
        except json.JSONDecodeError as exc:
            print(f"{ip}: invalid JSON response ({exc})")
