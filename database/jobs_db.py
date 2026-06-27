import json
import os

DB_FILE = "applied_jobs.json"


def load_db():
    if not os.path.exists(DB_FILE):
        return set()

    with open(DB_FILE, "r") as f:
        return set(json.load(f))


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(list(data), f)


def is_applied(job_id):
    db = load_db()
    return job_id in db


def mark_applied(job_id):
    db = load_db()
    db.add(job_id)
    save_db(db)
