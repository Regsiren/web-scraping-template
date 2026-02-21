import os
import requests
import re
from github import Github
from anthropic import Anthropic

# 1. SETUP: Load your keys from Railway's environment
GH_TOKEN = os.getenv("GITHUB_TOKEN")
ANTH_KEY = os.getenv("ANTHROPIC_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize the "Hands" and the "Brain"
g = Github(GH_TOKEN)
client = Anthropic(api_key=ANTH_KEY)

def telegram_alert(msg):
    """Sends a notification to your phone."""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def find_bounties():
    """Scans for open Algora bounties on GitHub."""
    query = 'label:bounty "algora" state:open'
    issues = g.search_issues(query=query, sort='created', order='desc')
    
    for issue in issues[:5]: # Check the latest 5
        # Look for £/$ signs in labels to find the reward amount
        labels = [l.name for l in issue.labels]
        reward = next((re.search(r'\d+', l).group() for l in labels if '$' in l or '£' in l), "TBD")
        
        if reward != "TBD" and int(reward) >= 150: # Only bother Remi for £150+
            telegram_alert(f"💰 *Bounty Found:* £{reward}\n*Project:* {issue.repository.name}\n[View Issue]({issue.html_url})")
            process_fix(issue, reward)

def process_fix(issue, reward):
    """Asks Claude 4.5 to draft a solution."""
    repo = issue.repository
    # Get the code context (simplified for this script)
    context = f"Repo: {repo.full_name}\nIssue: {issue.title}\nDescription: {issue.body}"
    
    # The Reasoning Step
    response = client.messages.create(
        model="claude-4-5-opus-20260210",
        max_tokens=2000,
        messages=[{"role": "user", "content": f"Draft a code fix for this GitHub issue:\n{context}"}]
    )
    
    fix_suggestion = response.content[0].text
    telegram_alert(f"✅ *AI Drafted a Fix for the £{reward} Bounty!*\nCheck the logs in Railway to review the code.")

if __name__ == "__main__":
    print("🚀 Remi's Bounty Bot is now scouting...")
    find_bounties()