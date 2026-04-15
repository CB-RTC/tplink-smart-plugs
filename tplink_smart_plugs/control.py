from __future__ import annotations

from tplink_smart_plugs.client import send_tplink_command


def set_plug_state(ip: str, state: bool) -> None:
    command = {"system": {"set_relay_state": {"state": int(state)}}}
    result = send_tplink_command(ip, command)
    err_code = result.get("system", {}).get("set_relay_state", {}).get("err_code")

    if err_code == 0:
        print(f"{ip}: {'ON' if state else 'OFF'}")
    else:
        print(f"{ip}: device returned err_code={err_code} | response={result}")
