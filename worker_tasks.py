from main import run_for_user

def process_user_jobs(user_id):
    print(f"🚀 Worker started for user {user_id}")
    run_for_user(user_id)
