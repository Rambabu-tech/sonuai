# tracker/tracker.py

import json
import os
from datetime import datetime

APPLICATIONS_FILE = "applications.json"

def load_applications():
    if not os.path.exists(APPLICATIONS_FILE):
        return []
    with open(APPLICATIONS_FILE, "r") as f:
        return json.load(f)

def save_all(applications):
    with open(APPLICATIONS_FILE, "w") as f:
        json.dump(applications, f, indent=2)

def already_applied(company, role):
    applications = load_applications()
    return any(
        a.get("company") == company and a.get("role") == role
        for a in applications
    )

def save_application(company, role, status="APPLIED"):
    applications = load_applications()

    applications.append({
        "company": company,
        "role": role,
        "status": status,
        "applied_at": datetime.now().isoformat()
    })

    save_all(applications)

def update_application_status(company, role, new_status):
    applications = load_applications()

    for app in applications:
        if app.get("company") == company and app.get("role") == role:
            app["status"] = new_status

    save_all(applications)
