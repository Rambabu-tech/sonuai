import requests

def auto_apply_ashby(job, applicant):
    try:
        files = {
            "resume": open(job["resume_path"], "rb")
        }

        data = {
            "first_name": applicant["first_name"],
            "last_name": applicant["last_name"],
            "email": applicant["email"]
        }

        response = requests.post(
            job["url"] + "/apply",
            data=data,
            files=files,
            timeout=15
        )

        if response.status_code in [200, 201]:
            print("✅ Ashby auto-apply successful")
            return True

        print("⚠️ Ashby apply failed:", response.status_code)
        return False

    except Exception as e:
        print("❌ Ashby error:", e)
        return False
