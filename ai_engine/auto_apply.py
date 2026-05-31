from playwright.sync_api import sync_playwright
import time

def apply_to_job(job_url, resume_path, user_email=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(job_url)
        time.sleep(3)

        try:
            # Example for Greenhouse-based sites
            if "greenhouse.io" in job_url:
                page.click("text=Apply")
                time.sleep(2)

                page.set_input_files("input[type='file']", resume_path)

                if user_email:
                    page.fill("input[type='email']", user_email)

                page.click("button[type='submit']")
                time.sleep(2)

                result = "Applied Successfully"

            else:
                result = "Unsupported Job Platform"

        except Exception as e:
            result = f"Failed: {str(e)}"

        browser.close()
        return result