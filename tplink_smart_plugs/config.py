from __future__ import annotations

from pathlib import Path


def load_addresses(file_path: str) -> list[str]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Address file not found: {path}")

    addresses: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue
        addresses.append(trimmed)

    if not addresses:
        raise ValueError(f"No addresses found in file: {path}")

    return addresses
