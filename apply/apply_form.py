from playwright.sync_api import sync_playwright

def apply_to_form(applicant, job_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(job_url)

        print("✅ Job page opened")
        print("🛑 Review & submit manually (browser stays open 2 minutes)")

        # Give YOU time to submit
        page.wait_for_timeout(120000)

        browser.close()
