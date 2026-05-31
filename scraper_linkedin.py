import json


def scrape_linkedin_jobs(keyword="DevOps Engineer"):
    print("🔍 Scraping LinkedIn jobs (mock mode)...")

    jobs = [
        {
            "company": "LinkedIn",
            "title": "DevOps Engineer",
            "description": "Looking for DevOps engineer with AWS, Kubernetes, Terraform experience.",
            "url": "https://www.linkedin.com/jobs/view/123456"
        }
    ]

    with open("linkedin_jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ Saved {len(jobs)} LinkedIn jobs")

    return jobs


