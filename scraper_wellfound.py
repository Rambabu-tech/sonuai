import json
import requests
from datetime import date

today = date.today().isoformat()

print("🔎 Scraping Wellfound jobs...\n")

url = "https://api.angel.co/1/jobs"

params = {
    "role": "devops",
    "remote": "true"
}

jobs = []

try:
    r = requests.get(url, params=params)
    data = r.json()

    for job in data.get("jobs", []):

        jobs.append({
            "title": job.get("title"),
            "company": job.get("startup_name"),
            "description": job.get("description", ""),
            "url": job.get("angellist_url"),
            "portal": "wellfound",
            "date_scraped": today
        })

    print("✅ Found", len(jobs), "Wellfound jobs")

except Exception as e:
    print("❌ Wellfound scraper failed:", e)

with open("wellfound_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("📁 Saved to wellfound_jobs.json")