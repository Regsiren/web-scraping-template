@app.route('/ping')
def ping():
    """Diagnostic trigger: Tells us exactly why Telegram is rejecting the message."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": "🔔 <b>Director's Signal:</b> Diagnostic Ping.",
        "parse_mode": "HTML"
    }
    
    try:
        res = requests.post(url, json=payload)
        data = res.json() # This gets the full error from Telegram
        
        if res.status_code == 200:
            return "<h1>Success!</h1><p>Check Telegram.</p>", 200
        else:
            # This will print the exact reason (e.g., 'chat not found' or 'bot was blocked')
            error_detail = data.get('description', 'Unknown Error')
            return f"<h1>Fail</h1><p>Telegram Error: {error_detail}</p>", 500
            
    except Exception as e:
        return f"<h1>Fail</h1><p>Connection Error: {str(e)}</p>", 500
