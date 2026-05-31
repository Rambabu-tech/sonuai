# mailbot/gmail_watcher.py

import time
from mailbot.gmail_confirm import find_application_confirmations
from tracker.tracker import update_application_status


def run_gmail_watcher():
    print("📡 Gmail watcher started and polling inbox every 60s")

    while True:
        try:
            confirmations = find_application_confirmations()

            if confirmations:
                for company in confirmations:
                    print(f"📬 Confirmation detected for {company}")
                    update_application_status(company, "CONFIRMED")
            else:
                print("📬 Checked inbox — 0 confirmation emails found")

        except Exception as e:
            print(f"⚠️ Gmail watcher error: {e}")

        time.sleep(60)


# ✅ THIS PART WAS MISSING
if __name__ == "__main__":
    run_gmail_watcher()
