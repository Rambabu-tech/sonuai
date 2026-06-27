from main import run_for_user

def process_user_jobs(user_id):
    run_for_user(user_id)
from concurrent.futures import ThreadPoolExecutor
from apply.apply_router import apply_to_job
from web.models import JobApplication
from extensions import db


def apply_single_job(job):
    try:
        print(f"🚀 Applying: {job.job_title}")

        result = apply_to_job(
            job.job_url,
            job.user.resume_path,
            job.cover_letter
        )

        job.status = result
        db.session.commit()

    except Exception as e:
        print("❌ Error:", e)


def process_pending_applications():

    jobs = JobApplication.query.filter_by(status="MATCHED").limit(20).all()

    print(f"📦 Jobs fetched for worker: {len(jobs)}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(apply_single_job, jobs)
