# TP-Link Smart Plugs (Raw TCP)

Control TP-Link smart plugs directly over a raw TCP socket using TP-Link's XOR protocol.

By default, plug IPs are read from `ips.txt` (one IP per line).

## Usage

Turn all default plugs on:

```powershell
python main.py on
```

Turn all default plugs off:

```powershell
python main.py off
```

Control specific IPs (override file values):

```powershell
python main.py on --ips 192.168.0.193 192.168.0.195
python main.py off --ips 192.168.0.196
```

Use a custom IP file:

```powershell
python main.py on --ips-file .\my-plugs.txt
```

## Notes

- Uses TCP port `9999`.
- Devices must be reachable on the local network.
- Runtime entrypoint is `main.py`, with logic split into modules under `tplink_smart_plugs/`.
