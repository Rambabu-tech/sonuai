import sys
import os
import time
from dotenv import load_dotenv

from flask import Flask
from extensions import db
from web.models import User, JobApplication

from ai_engine.matcher import compute_similarity, decide_application
from ai_engine.cover_letter import generate_cover_letter
from ai_engine.skill_extractor import extract_skills
from ai_engine.resume_parser import read_resume
from ai_engine.role_detector import detect_role

from job_sources import fetch_all_jobs
from apply.auto_apply import apply_to_job  # ✅ IMPORTANT


# ✅ ENV
load_dotenv()
print("🔥 KEY:", os.getenv("OPENAI_API_KEY")[:15])


def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, "instance", "site.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)

    return app


def run_for_user(user_id):

    app = create_app()

    with app.app_context():

        print(f"\n🚀 Running SonuAI for user {user_id}\n")

        user = db.session.get(User, user_id)

        if not user:
            print("❌ User not found")
            return

        resume_path = user.resume_path or "uploads/default_resume.txt"

        if not os.path.exists(resume_path):
            print("❌ Resume missing")
            return

        # ✅ READ RESUME
        resume_content = read_resume(resume_path)[:2000]
        print("📄 Resume preview:", resume_content[:200])

        # ✅ EXTRACT SKILLS
        skills = extract_skills(resume_content)
        skills = [s.lower().strip() for s in skills if len(s) < 30]

        if not skills:
            skills = ["software", "developer", "engineer"]

        print("🧠 Skills:", skills[:15])

        # ✅ DETECT ROLE (ONLY ONCE — FIX)
        roles = detect_role(resume_content)
        print("🎯 Detected roles:", roles)

        # 🚀 FETCH JOBS
        jobs = fetch_all_jobs()
        print(f"🔎 Jobs fetched: {len(jobs)}")

        jobs = [j for j in jobs if j.get("title") and j.get("description")]

        # ✅ PRIORITIZE BETTER JOBS
        jobs = sorted(jobs, key=lambda j: len(j.get("description", "")), reverse=True)

        seen = set()
        unique_jobs = []

        for j in jobs:
            key = (j.get("title"), j.get("company"))
            if key not in seen:
                seen.add(key)
                unique_jobs.append(j)

        jobs = unique_jobs[:100]


        processed = 0
        matched = 0

        # ✅ APPLY CONTROL (VERY IMPORTANT)
        applied_count = 0
        MAX_APPLY = 20

        for job in jobs:

            if applied_count >= MAX_APPLY:
                print("🛑 Apply limit reached")
                break

            title = (job.get("title") or "").lower()
            description = (job.get("description") or "").lower()
            company = job.get("company", "")
            url = job.get("url", "")

            print(f"\n👉 Checking: {title}")

            # 🚀 STEP 1 — REMOVE BUSINESS ROLES
            bad_roles = [
                "account executive", "sales", "marketing",
                "finance", "hr", "recruiter",
                "operations", "customer", "business",
                "manager", "director"
            ]

            if any(role in title for role in bad_roles):
                print(f"❌ Skip business role: {title}")
                continue

            # 🚀 STEP 2 — REQUIRE TECH ROLE
            good_roles = [
                "engineer", "developer", "software",
                "backend", "frontend", "full stack",
                "data", "machine learning",
                "api", "cloud"
            ]

            if not any(role in title for role in good_roles):
                print(f"⚠️ Not tech role: {title}")
                continue

            # 🚀 STEP 3 — SKILL MATCH
            skill_match_count = sum(
                1 for skill in skills[:15] if skill in description
            )

            if skill_match_count < 1:
                continue

            # 🚀 STEP 4 — QUALITY FILTER
            if len(description) < 200:
                continue

            processed += 1
            time.sleep(0.3)

            print(f"🔍 {title} @ {company}")
            print(f"🧠 Skill matches: {skill_match_count}")

            try:
                # 🚀 STEP 5 — AI MATCH
                score = compute_similarity(resume_content, description)

                if score < 0.35:
                    print(f"⛔ Low match ({score:.2f})")
                    continue

                matched += 1
                decision = decide_application(score)

                print(f"📊 Score: {score:.2f} → {decision}")

                status = "SKIPPED"
                cover_letter = ""

                # 🚀 APPLY LOGIC (REAL FIX)
                if decision == "APPLY":

                    try:
                        cover_letter = generate_cover_letter(
                            resume_content,
                            title,
                            description[:1200]
                        )
                    except Exception as e:
                        print("⚠️ Cover error:", e)

                    # 🔥 REAL AUTO APPLY
                    result = apply_to_job(url, resume_path, cover_letter)

                    if result == "APPLIED":
                        status = "APPLIED"
                        applied_count += 1
                    elif result == "FAILED":
                        status = "FAILED"
                    else:
                        status = "MANUAL"

                # 🚀 SAVE TO DB
                db.session.add(JobApplication(
                    user_id=user.id,
                    job_title=title,
                    job_url=url,
                    company=company,
                    score=score,
                    decision=decision,
                    status=status,
                    cover_letter=cover_letter,
                    source="multi-source"
                ))

            except Exception as e:
                print("❌ Error:", e)

        db.session.commit()

        print(f"\n🎯 Processed: {processed}")
        print(f"✅ Matched: {matched}")
        print(f"🚀 Applied: {applied_count}")
        print("\n🎉 DONE\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Provide user ID")
        sys.exit(1)

    run_for_user(int(sys.argv[1]))