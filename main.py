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

# 🔥 Load env
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# 🔥 Create app (no circular import)
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///site.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    return app


# 🔥 MAIN LOGIC
def run_for_user(user_id):

    app = create_app()

    with app.app_context():

        print(f"\n🚀 Starting AI Job Engine for user {user_id}\n")

        user = db.session.get(User, user_id)

        if not user:
            print("❌ User not found")
            return

        # ✅ Resume
        resume_path = user.resume_path or "uploads/default_resume.txt"
        resume_path = os.path.abspath(resume_path)

        if not os.path.exists(resume_path):
            print("❌ Resume file missing")
            return

        with open(resume_path, "r", encoding="utf-8", errors="ignore") as f:
            resume_content = f.read()

        print("✅ Resume loaded")

        # ✅ Load jobs
        jobs = []
        files = [
            "linkedin_jobs.json",
            "jobs.json",
            "lever_jobs.json",
            "remoteok_jobs.json"
        ]

        for file in files:
            if os.path.exists(file):
                try:
                    with open(file) as f:
                        jobs.extend(json.load(f))
                except:
                    pass

        print(f"\n🔎 Processing {len(jobs)} jobs...\n")

        seen_urls = set()
        results = []

        output_file = f"applications_{user.id}.json"

        # ✅ Dedup
        if os.path.exists(output_file):
            with open(output_file) as f:
                old = json.load(f)
                seen_urls = {j.get("url") for j in old}

        for job in jobs:

            title = job.get("title", "")
            company = job.get("company", "")
            description = job.get("description", "")
            url = job.get("url", "")

            if not url or url in seen_urls:
                print("⚠️ Already applied:", title)
                continue

            print(f"\n🔍 {title} @ {company}")

            try:
                # 🚀 AI MATCHING (THIS IS YOUR STEP 2 FIX)
                score = compute_similarity(resume_content, description)
                decision = decide_application(score)

                print(f"📊 Score: {score:.3f} | Decision: {decision}")

                status = "SKIPPED"

                if decision == "APPLY":

                    try:
                        cover_letter = generate_cover_letter(
                            resume_content, title, description
                        )
                    except:
                        cover_letter = ""

                    # ⚠️ Disable Selenium on Render
                    if os.getenv("RENDER") == "true":
                        print("⚠️ Skipping auto apply (Render)")
                        applied = False
                    else:
                        applied = apply_to_job(url, resume_path, cover_letter)

                    status = "APPLIED" if applied else "FAILED"

                # ✅ Save DB
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
                    "decision": decision,
                    "status": status,
                    "url": url
                })

            except Exception as e:
                print("❌ Error:", e)

        db.session.commit()

        # ✅ Save JSON
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n📁 Saved → {output_file}")
        print("\n🎯 DONE\n")


# 🔥 CLI SUPPORT
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Provide user ID")
        sys.exit(1)

    run_for_user(int(sys.argv[1]))