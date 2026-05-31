import json
import requests
from datetime import date


# -------------------------------------------------
# LEVER JOB BOARDS
# -------------------------------------------------

LEVER_COMPANIES = {
    "netflix": "Netflix",
    "shopify": "Shopify",
    "plaid": "Plaid",
    "figma": "Figma",
    "robinhood": "Robinhood"
}


# -------------------------------------------------
# DEVOPS FILTER
# -------------------------------------------------

DEVOPS_KEYWORDS = [
    "devops",
    "site reliability",
    "sre",
    "platform",
    "infrastructure",
    "cloud",
    "kubernetes",
    "docker",
]


def is_devops_job(title):
    title = title.lower()
    return any(keyword in title for keyword in DEVOPS_KEYWORDS)


# -------------------------------------------------
# SCRAPER
# -------------------------------------------------

today = date.today().isoformat()
jobs = []

print("🔎 Scraping Lever job boards...\n")

for company_slug, company_name in LEVER_COMPANIES.items():

    api_url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"

    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            print(f"❌ API error for {company_name}")
            continue

        data = response.json()

    except Exception as e:
        print(f"❌ Request failed for {company_name}: {e}")
        continue

    company_count = 0

    for job in data:

        title = job.get("text", "")

        if not is_devops_job(title):
            continue

        jobs.append({
            "title": f"{title} - {today}",
            "company": company_name,
            "description": job.get("descriptionPlain", ""),
            "url": job.get("hostedUrl"),
            "job_id": job.get("id"),
            "portal": "lever"
        })

        company_count += 1

    print(f"✅ {company_name}: {company_count} DevOps jobs found")


# -------------------------------------------------
# SAVE RESULTS
# -------------------------------------------------

with open("lever_jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("\n🎯 Total Lever DevOps jobs:", len(jobs))
print("📁 Saved to lever_jobs.json")