import requests
import json
from datetime import date

REMOTEOK_API = "https://remoteok.com/api"

DEVOPS_KEYWORDS = [
    "devops",
    "site reliability",
    "sre",
    "platform engineer",
    "cloud engineer",
    "infrastructure engineer"
]


def is_devops(title):
    title = title.lower()
    return any(k in title for k in DEVOPS_KEYWORDS)


print("🔎 Scraping RemoteOK jobs...")

response = requests.get(
    REMOTEOK_API,
    headers={"User-Agent": "Mozilla/5.0"}
)

data = response.json()

jobs = []
today = date.today().isoformat()

for job in data:

    title = job.get("position", "")

    if not is_devops(title):
        continue

    jobs.append({
        "title": title,
        "company": job.get("company"),
        "description": job.get("description", ""),
        "url": job.get("url"),
        "portal": "remoteok",
        "date_scraped": today
    })

print(f"✅ Found {len(jobs)} DevOps jobs")

with open("remoteok_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("📁 Saved to remoteok_jobs.json")