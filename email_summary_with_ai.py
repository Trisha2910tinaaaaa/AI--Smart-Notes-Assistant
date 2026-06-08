import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
client = Groq()

def get_todays_notes():
    if not os.path.exists("notes.json"):
        return []
    
    with open("notes.json", "r") as f:
        notes = json.load(f)
    
    today = datetime.now().date()
    result = []
    
    for note in notes:
        if isinstance(note, dict):
            ts = note.get("timestamp")
            if ts:
                note_date = datetime.fromisoformat(ts).date()
                if note_date == today:
                    result.append({
                        "text": note.get("text", ""),
                        "category": note.get("category", "general")
                    })
    return result

def get_ai_insight(notes):
    if not notes:
        return "No notes today. Add some to get insights!"
    
    notes_text = "\n".join([f"- {n['text']}" for n in notes])
    
    prompt = f"""These are my notes from today:
{notes_text}

Give me ONE short, helpful insight or reminder based on these notes. Max 20 words."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content

def send_email(subject, body):
    msg = MIMEText(body, "plain")
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = subject
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()

def main():
    notes = get_todays_notes()
    insight = get_ai_insight(notes)
    
    if notes:
        note_lines = "\n".join([f"• {n['text']}" for n in notes])
        body = f"""Good morning!

Here's what you noted yesterday:

{note_lines}

🤖 AI Insight: {insight}

---
Your Second Brain AI
"""
    else:
        body = f"""Good morning!

You didn't add any notes yesterday.

Add notes today to get AI insights tomorrow!

---
Your Second Brain AI
"""
    
    send_email(f"Daily Note Summary - {datetime.now().strftime('%b %d')}", body)
    print(f"✅ Email sent at {datetime.now()}")

if __name__ == "__main__":
    main()