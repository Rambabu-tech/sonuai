import json
import os

def load_json_file(filename):
    try:
        if not os.path.exists(filename):
            return []

        with open(filename, "r") as f:
            return json.load(f)

    except Exception as e:
        print(f"❌ Error reading {filename}:", e)
        return []


def fetch_all_jobs():

    print("📦 Loading jobs from all sources...")

    all_jobs = []

    sources = [
        "jobs.json",              # greenhouse
        "lever_jobs.json",
        "workday_jobs.json",
        "yc_jobs.json",
        "wellfound_jobs.json",
        "linkedin_jobs.json",
        "indeed_jobs.json"
    ]

    for file in sources:
        jobs = load_json_file(file)

        print(f"✅ {file}: {len(jobs)} jobs")

        all_jobs.extend(jobs)

    print(f"\n🎯 Total jobs collected: {len(all_jobs)}\n")

    return all_jobs

