import requests
from bs4 import BeautifulSoup
import json
from datetime import date

URL = "https://www.indeed.com/jobs?q=devops+engineer&l=United+States"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("🔎 Scraping Indeed jobs...")

response = requests.get(URL, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

jobs = []
today = date.today().isoformat()

for card in soup.select(".job_seen_beacon"):

    title_tag = card.select_one("h2")
    company_tag = card.select_one(".companyName")

    if not title_tag or not company_tag:
        continue

    title = title_tag.text.strip()
    company = company_tag.text.strip()

    jobs.append({
        "title": title,
        "company": company,
        "description": "",
        "url": "https://www.indeed.com",
        "portal": "indeed",
        "date_scraped": today
    })

print(f"✅ Found {len(jobs)} Indeed jobs")

with open("indeed_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("📁 Saved to indeed_jobs.json")