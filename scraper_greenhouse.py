import json
import requests
from datetime import date
from bs4 import BeautifulSoup

GREENHOUSE_COMPANIES = {
    "stripe": "Stripe",
    "airbnb": "Airbnb",
    "coinbase": "Coinbase",
    "databricks": "Databricks",
    "snowflake": "Snowflake",
    "notion": "Notion",
    "figma": "Figma",
    "openai": "OpenAI",
    "discord": "Discord",
    "doordash": "DoorDash"
}

EXCLUDE_KEYWORDS = [
    "sales", "marketing", "recruiter",
    "hr", "assistant", "coordinator",
    "customer support", "writer"
]

def is_valid_job(title):
    title = title.lower()
    if any(x in title for x in EXCLUDE_KEYWORDS):
        return False
    return True


def get_full_job_description(job_url):
    try:
        page = requests.get(job_url, timeout=10)
        if page.status_code != 200:
            return ""

        soup = BeautifulSoup(page.text, "html.parser")
        return soup.get_text(" ", strip=True)[:5000]

    except Exception as e:
        print("⚠️ Description fetch error:", e)
        return ""


# ------------------------------
# MAIN
# ------------------------------

today = date.today().isoformat()
jobs = []
seen_jobs = set()

print("🔎 Scraping ALL jobs...\n")

for board, company_name in GREENHOUSE_COMPANIES.items():

    print(f"➡️ Fetching {company_name}...")

    api_url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

    try:
        response = requests.get(api_url, timeout=10)

        print(f"   Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Failed for {company_name}")
            continue

        data = response.json()

    except Exception as e:
        print(f"❌ Error fetching {company_name}: {e}")
        continue

    company_count = 0

    for job in data.get("jobs", []):

        title = job.get("title", "")

        if not is_valid_job(title):
            continue

        job_id = job.get("id")

        if job_id in seen_jobs:
            continue

        seen_jobs.add(job_id)

        job_url = f"https://boards.greenhouse.io/{board}/jobs/{job_id}"

        print(f"   🔹 Found: {title}")

        description = get_full_job_description(job_url)

        jobs.append({
            "title": title,
            "company": company_name,
            "description": description,
            "url": job_url,
            "portal": "greenhouse",
            "date_scraped": today
        })

        company_count += 1

    print(f"✅ {company_name}: {company_count} jobs\n")


# SAVE
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("\n🎯 Total jobs saved:", len(jobs))
print("📁 Saved to jobs.json")