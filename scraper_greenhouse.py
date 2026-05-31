import json
import requests
from datetime import date
from bs4 import BeautifulSoup

# -------------------------------------------------
# GREENHOUSE BOARDS
# -------------------------------------------------

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

# -------------------------------------------------
# DEVOPS ROLE KEYWORDS
# -------------------------------------------------

DEVOPS_KEYWORDS = [
    "devops",
    "site reliability",
    "sre",
    "platform engineer",
    "cloud engineer",
    "infrastructure engineer",
    "production engineer",
    "kubernetes engineer",
    "build engineer",
    "release engineer",
    "systems engineer"
]

# -------------------------------------------------
# EXCLUDE NON ENGINEERING ROLES
# -------------------------------------------------

EXCLUDE_KEYWORDS = [
    "manager",
    "director",
    "product",
    "sales",
    "account",
    "marketing",
    "customer",
    "business",
    "technical writer",
    "support",
    "recruiter"
]

# -------------------------------------------------
# FILTER FUNCTIONS
# -------------------------------------------------

def is_devops_job(title):
    """
    Determine if job title is DevOps related
    """

    title = title.lower()

    if not any(k in title for k in DEVOPS_KEYWORDS):
        return False

    if any(x in title for x in EXCLUDE_KEYWORDS):
        return False

    return True


# -------------------------------------------------
# FETCH FULL JOB DESCRIPTION
# -------------------------------------------------

def get_full_job_description(job_url):
    """
    Scrape full job description from job page
    """

    try:

        page = requests.get(job_url, timeout=10)

        if page.status_code != 200:
            return ""

        soup = BeautifulSoup(page.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        return text[:8000]  # limit size

    except Exception:
        return ""


# -------------------------------------------------
# SCRAPER
# -------------------------------------------------

today = date.today().isoformat()

jobs = []

seen_jobs = set()

print("🔎 Scraping Greenhouse job boards...\n")

for board, company_name in GREENHOUSE_COMPANIES.items():

    api_url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

    try:

        response = requests.get(api_url, timeout=10)

        if response.status_code != 200:
            print(f"❌ API error for {company_name}")
            continue

        data = response.json()

    except Exception as e:
        print(f"❌ Request failed for {company_name}: {e}")
        continue

    company_count = 0

    for job in data.get("jobs", []):

        title = job.get("title", "")

        if not is_devops_job(title):
            continue

        job_id = job.get("id")

        if job_id in seen_jobs:
            continue

        seen_jobs.add(job_id)

        job_url = f"https://boards.greenhouse.io/{board}/jobs/{job_id}"

        # Fetch full description
        description = get_full_job_description(job_url)

        jobs.append({
            "title": title,
            "company": company_name,
            "description": description,
            "url": job_url,
            "job_id": job_id,
            "board": board,
            "portal": "greenhouse",
            "date_scraped": today
        })

        company_count += 1

    print(f"✅ {company_name}: {company_count} DevOps jobs found")


# -------------------------------------------------
# SAVE RESULTS
# -------------------------------------------------

with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("\n🎯 Total DevOps jobs saved:", len(jobs))
print("📁 Saved to jobs.json")