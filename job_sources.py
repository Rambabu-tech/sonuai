import requests

def fetch_remoteok_jobs():

    url = "https://remoteok.com/api"

    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla"})
        data = res.json()

        jobs = []

        for job in data[1:]:  # skip metadata
            jobs.append({
                "title": job.get("position"),
                "company": job.get("company"),
                "description": job.get("description", ""),
                "url": job.get("url")
            })

        return jobs

    except Exception as e:
        print("❌ Job fetch error:", e)
        return []
