import json
import smtplib
from email.mime.text import MIMEText

with open("applications_1.json") as f:
    jobs = json.load(f)

apply_jobs = [j for j in jobs if j["decision"] == "APPLY"]

body = ""

for j in apply_jobs:
    body += f"{j['title']} - {j['company']}\n\n"

msg = MIMEText(body)
msg["Subject"] = "Daily DevOps Jobs"
msg["From"] = "rambabukurva899@gmail.com"
msg["To"] = "rambabukurva899@gmail.com"

s = smtplib.SMTP("smtp.gmail.com", 587)
s.starttls()
s.login("rambabukurva899@gmail.com", "Rambabu2026@")
s.send_message(msg)
s.quit()