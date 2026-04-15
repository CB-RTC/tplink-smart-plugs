# TP-Link Smart Plugs (Raw TCP)

Control TP-Link smart plugs directly over a raw TCP socket using TP-Link's XOR protocol.

Default plug IPs are:
- `192.168.0.193`
- `192.168.0.195`
- `192.168.0.196`

## Usage

Turn all default plugs on:

```powershell
python main.py on
```

Turn all default plugs off:

```powershell
python main.py off
```

Control specific IPs:

```powershell
python main.py on --ips 192.168.0.193 192.168.0.195
python main.py off --ips 192.168.0.196
```

## Notes

- Uses TCP port `9999`.
- Devices must be reachable on the local network.
