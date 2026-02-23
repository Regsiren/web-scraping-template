import os
import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

# Config from Railway Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_msg(message):
    """Core communication channel for the Scout fleet."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        return False

@app.route('/ping')
def ping():
    """Manual trigger: Confirm Telegram is talking to Bot 1."""
    test_msg = "🔔 <b>Director's Signal:</b> Bot 1 (Bounty Scout) is Online and healthy."
    success = send_telegram_msg(test_msg)
    if success:
        return "<h1>Success!</h1><p>Check Telegram. The bot is talking.</p>", 200
    else:
        return "<h1>Fail</h1><p>Telegram rejected the message. Check logs.</p>", 500

@app.route('/')
def home():
    return "<h1>Bot 1: Bounty Scout</h1><p>Status: Monitoring...</p>", 200

def scout_bounties():
    """Background task: Keeps scouting running 24/7."""
    time.sleep(10) # Wait for server boot
    send_telegram_msg("🚀 <b>System Boot:</b> Bounty Scout logic is now running.")
    
    while True:
        try:
            print("🔍 Scouting for new opportunities...")
            # Placeholder for scouting logic
            time.sleep(3600)
        except Exception as e:
            print(f"Scout Error: {e}")
            time.sleep(600)

# Start background thread immediately
threading.Thread(target=scout_bounties, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
