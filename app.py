from flask import Flask, jsonify, send_file
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

# Replace with your Pi-hole IP and password
PIHOLE = 'http://IP_ADDRESS'
PASSWORD = 'PIHOLE_PASSWORD'

# Session cache
cached_sid = None
sid_expiry = 0
SESSION_LIFETIME = 270  # seconds (5 min timeout minus 30s buffer)

def get_sid():
    global cached_sid, sid_expiry
    if cached_sid and time.time() < sid_expiry:
        return cached_sid
    auth = requests.post(f'{PIHOLE}/api/auth', json={'password': PASSWORD})
    cached_sid = auth.json()['session']['sid']
    sid_expiry = time.time() + SESSION_LIFETIME
    return cached_sid

@app.route('/')
def home():
    return 'Pi-hole API is running!'

@app.route('/widget')
def widget():
    return send_file('widget.html')

@app.route('/pihole')
def pihole_stats():
    sid = get_sid()
    stats = requests.get(f'{PIHOLE}/api/stats/summary', headers={'X-FTL-SID': sid})
    return jsonify(stats.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
