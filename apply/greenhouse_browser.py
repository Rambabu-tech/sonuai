import webbrowser
import time


def open_greenhouse_for_manual_submit(job_url: str):
    """
    Jobright-style manual apply:
    - Opens the real Greenhouse job page
    - User clicks Submit
    - Greenhouse sends confirmation email
    """

    if not job_url:
        raise ValueError("Missing job URL")

    print("🌐 Opening Greenhouse job page...")
    webbrowser.open(job_url)

    print("🛑 MANUAL APPLY REQUIRED")
    print("👉 Submit the application in the browser")
    input("▶ Press ENTER after you finish submitting...")
    time.sleep(1)
