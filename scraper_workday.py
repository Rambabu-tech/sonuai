import json
import requests
from datetime import date

print("🔎 Scraping Workday jobs...")

WORKDAY_COMPANIES = {
    "snowflake": "https://snowflake.wd5.myworkdayjobs.com/en-US/SnowflakeCareers/jobs",
    "nvidia": "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/jobs",
    "okta": "https://okta.wd5.myworkdayjobs.com/en-US/Okta_Jobs/jobs"
}

DEVOPS_KEYWORDS = [
    "devops",
    "site reliability",
    "sre",
    "platform",
    "cloud",
    "infrastructure",
    "kubernetes"
]

jobs = []
today = date.today().isoformat()

for company, url in WORKDAY_COMPANIES.items():

    try:

        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ API error for {company}")
            continue

        data = response.json()

    except Exception:
        print(f"⚠️ Could not fetch {company}")
        continue

    count = 0

    for job in data.get("jobPostings", []):

        title = job.get("title", "").lower()

        if not any(k in title for k in DEVOPS_KEYWORDS):
            continue

        jobs.append({
            "title": job.get("title"),
            "company": company.capitalize(),
            "description": job.get("externalPath", ""),
            "url": url,
            "portal": "workday"
        })

        count += 1

    print(f"✅ {company}: {count} DevOps jobs")

with open("workday_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print(f"\n🎯 Total Workday jobs saved: {len(jobs)}")