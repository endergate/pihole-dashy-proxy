# pihole-dashy-proxy

A lightweight Flask proxy that bridges Pi-hole v6 and Dashy. Pi-hole v6 introduced session-based authentication which broke Dashy's native Pi-hole widget. This project works around that by running a small Python API that handles the v6 auth and serves a custom HTML stats widget that Dashy can load via iframe.

## What it does

- Authenticates with Pi-hole v6's session-based API
- Caches the session for 270 seconds to avoid hitting Pi-hole's API seat limit
- Serves a live stats widget showing queries, blocked, blocklist size, and active clients
- Runs as a systemd service so it starts automatically on boot

## Prerequisites

- Ubuntu Server
- Python 3
- Pi-hole v6 running on your network (bare metal or Docker)
- Dashy running on your network

## Project structure
```
pihole-api/
├── app.py          # Flask proxy and API
├── widget.html     # Stats widget served to Dashy via iframe
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/endergate/pihole-dashy-proxy.git
cd pihole-dashy-proxy
```

### 2. Create a virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors requests
```

### 3. Configure your credentials

Edit `app.py` and replace the placeholders with your actual values:
```python
PIHOLE = 'http://YOUR_PIHOLE_IP'
PASSWORD = 'YOUR_PIHOLE_PASSWORD'
```

### 4. Create the systemd service
```bash
sudo nano /etc/systemd/system/pihole-api.service
```

Paste this in:
```ini
[Unit]
Description=Pi-hole Stats API
After=network.target

[Service]
User=server
WorkingDirectory=/home/server/scripts/pihole-api
ExecStart=/home/server/scripts/pihole-api/venv/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then enable and start it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pihole-api
sudo systemctl start pihole-api
```

### 5. Configure Dashy

Add this to your Dashy `conf.yml`:
```yaml
- name: Pi-hole
  icon: hl-pihole
  widgets:
    - type: iframe
      options:
        url: http://YOUR_SERVER_IP:5000/widget
        frameHeight: 220
```

Restart Dashy:
```bash
sudo docker restart dashy
```

## Increasing Pi-hole session limit (optional)

If you hit API seat errors run this on your Pi-hole server:
```bash
sudo docker exec pihole pihole-FTL --config webserver.api.max_sessions 16
sudo docker restart pihole
```

## License

MIT
