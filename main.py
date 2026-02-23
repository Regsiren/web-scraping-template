import os
import requests
import time
import threading
from flask import Flask

# --- 1. DEFINE THE APP FIRST ---
app = Flask(__name__)

# Config from Railway Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_msg(message):
    """Core communication channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        res = requests.post(url, json=payload)
        return res
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

# --- 2. THE DIAGNOSTIC ROUTES ---
@app.route('/ping')
def ping():
    """Diagnostic trigger: Tells us EXACTLY why Telegram says no."""
    res = send_telegram_msg("🔔 <b>Director's Signal:</b> Diagnostic Ping.")
    
    if res is None:
        return "<h1>Fail</h1><p>Could not connect to Telegram servers.</p>", 500
    
    data = res.json()
    if res.status_code == 200:
        return "<h1>Success!</h1><p>Check Telegram.</p>", 200
    else:
        # This extracts the specific error (e.g., 'Unauthorized' or 'chat not found')
        error_msg = data.get('description', 'Unknown Error')
        return f"<h1>Fail</h1><p>Telegram Error: {error_msg}</p>", 500

@app.route('/')
def home():
    return "<h1>Bot 1: Bounty Scout</h1><p>Status: Monitoring...</p>", 200

# --- 3. THE BACKGROUND SCOUT ---
def scout_bounties():
    """Keeps the logic running while the web server stays awake."""
    time.sleep(10)
    print("🚀 System Boot: Scout logic active.")
    while True:
        try:
            # Scouting placeholder
            time.sleep(3600)
        except Exception as e:
            time.sleep(600)

threading.Thread(target=scout_bounties, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
