import json
import requests
from datetime import date

today = date.today().isoformat()

print("🔎 Scraping YC jobs...\n")

url = "https://www.ycombinator.com/api/jobs"

jobs = []

try:
    r = requests.get(url)
    data = r.json()

    for job in data.get("jobs", []):

        title = job.get("title", "").lower()

        if "devops" in title or "platform" in title or "sre" in title or "infrastructure" in title:

            jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "description": job.get("description", ""),
                "url": job.get("url"),
                "portal": "yc",
                "date_scraped": today
            })

    print("✅ Found", len(jobs), "YC jobs")

except Exception as e:
    print("❌ YC scraper failed:", e)

with open("yc_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("📁 Saved to yc_jobs.json")