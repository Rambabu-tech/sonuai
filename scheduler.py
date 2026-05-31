import time
import subprocess
from web.app import app
from web.models import User

INTERVAL = 60 * 60

running = set()


def run_all():
    with app.app_context():
        users = User.query.all()

        for user in users:

            if not user.resume_path:
                print(f"❌ Skip user {user.id}")
                continue

            if user.id in running:
                print(f"⚠️ Already running user {user.id}")
                continue

            print(f"👤 Running user {user.id}")

            subprocess.Popen(["python", "main.py", str(user.id)])

            running.add(user.id)


while True:
    print("\n🚀 Scheduler started\n")
    run_all()
    print("⏳ Sleeping...\n")
    time.sleep(INTERVAL)