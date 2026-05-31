import sys
import os
import json
from dotenv import load_dotenv

from flask import Flask
from extensions import db
from web.models import User, JobApplication

from ai_engine.matcher import compute_similarity, decide_application
from ai_engine.cover_letter import generate_cover_letter
from apply.auto_apply import apply_to_job
from job_sources import fetch_remoteok_jobs

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///site.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    return app


def run_for_user(user_id):

    app = create_app()

    with app.app_context():

        print(f"\n🚀 Running SonuAI for user {user_id}\n")

        user = db.session.get(User, user_id)

        if not user:
            return

        resume_path = user.resume_path or "uploads/default_resume.txt"

        if not os.path.exists(resume_path):
            return

        with open(resume_path, "r", encoding="utf-8", errors="ignore") as f:
            resume_content = f.read()

        jobs = fetch_remoteok_jobs()

        results = []

        for job in jobs:

            title = job.get("title", "")
            company = job.get("company", "")
            description = job.get("description", "")
            url = job.get("url", "")

            score = compute_similarity(resume_content, description)
            decision = decide_application(score)

            status = "SKIPPED"

            if decision == "APPLY":

                try:
                    cover_letter = generate_cover_letter(
                        resume_content, title, description
                    )
                except:
                    cover_letter = ""

                # ⚠️ Render safe (no Selenium)
                if os.getenv("RENDER") == "true":
                    applied = False
                else:
                    applied = apply_to_job(url, resume_path, cover_letter)

                status = "APPLIED" if applied else "FAILED"

            db.session.add(JobApplication(
                user_id=user.id,
                job_title=title,
                job_url=url,
                company=company,
                score=score,
                decision=decision
            ))

            results.append({
                "title": title,
                "company": company,
                "score": round(score, 3),
                "status": status,
                "url": url
            })

        db.session.commit()

        with open(f"applications_{user.id}.json", "w") as f:
            json.dump(results, f, indent=2)