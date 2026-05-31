from apply.greenhouse_apply import apply_greenhouse
from apply.lever_apply import apply_lever
import webbrowser


def apply_to_job(job_url, resume_path, cover_letter):

    if not job_url:
        return False

    url = job_url.lower()

    try:

        if "greenhouse.io" in url:
            return apply_greenhouse(job_url, resume_path)

        elif "lever.co" in url:
            return apply_lever(job_url, resume_path, cover_letter)

        elif "linkedin.com" in url:
            webbrowser.open(job_url)
            return "MANUAL"

        elif "remoteok.com" in url:
            webbrowser.open(job_url)
            return "MANUAL"

        else:
            webbrowser.open(job_url)
            return "MANUAL"

    except Exception as e:
        print("❌ Apply error:", e)
        return False