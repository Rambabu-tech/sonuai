import json
import requests
from datetime import date

today = date.today().isoformat()

print("🔎 Scraping Dice jobs...\n")

jobs = []

url = "https://www.dice.com/api/jobs/search"

params = {
    "q": "devops",
    "location": "United States",
    "countryCode2": "US",
    "radius": "30",
    "page": 1,
    "pageSize": 50
}

try:
    response = requests.get(url, params=params)

    data = response.json()

    for job in data.get("data", []):

        jobs.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "description": job.get("description", ""),
            "url": job.get("detailUrl"),
            "portal": "dice",
            "date_scraped": today
        })

    print("✅ Found", len(jobs), "Dice jobs")

except Exception as e:
    print("❌ Dice scraper failed:", e)

with open("dice_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("📁 Saved to dice_jobs.json")