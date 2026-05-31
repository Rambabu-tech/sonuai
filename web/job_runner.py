import subprocess

running_jobs = {}

def start_job(user_id):

    user_id = str(user_id)

    if user_id in running_jobs:
        return

    log_file = f"job_{user_id}.log"

    with open(log_file, "w") as f:
        process = subprocess.Popen(
            ["python", "main.py", user_id],
            stdout=f,
            stderr=f
        )

    running_jobs[user_id] = process.pid


def get_status(user_id):
    return "Running" if str(user_id) in running_jobs else "Idle"


def get_log_file(user_id):
    return f"job_{user_id}.log"