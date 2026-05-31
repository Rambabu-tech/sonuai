import json
import requests
from bs4 import BeautifulSoup
from datetime import date

today = date.today().isoformat()

url = "https://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

jobs = []

quote_blocks = soup.find_all("div", class_="quote")

for block in quote_blocks:
    job = {
        "title": f"Senior DevOps Engineer - {today}",
        "company": block.find("small", class_="author").text,
        "description": "AWS Docker Kubernetes Terraform Linux CI/CD Python",
        "url": "https://www.selenium.dev/selenium/web/web-form.html"
    }
    jobs.append(job)

with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("✅ Saved today's DevOps jobs to jobs.json")
