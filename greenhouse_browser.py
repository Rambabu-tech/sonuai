from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os


def open_greenhouse_for_manual_submit(job_url: str, resume_path: str):
    """
    Opens Greenhouse job page, uploads resume if possible,
    waits for user to click Submit.
    """

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(job_url)

    time.sleep(5)

    # Try resume upload (optional)
    try:
        upload = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        upload.send_keys(os.path.abspath(resume_path))
        print("✅ Resume uploaded")
        time.sleep(3)
    except:
        print("ℹ️ Resume upload skipped (not required or already uploaded)")

    print("\n🟡 ACTION REQUIRED")
    print("👉 Fill remaining fields if any")
    print("👉 CLICK SUBMIT to receive confirmation email")
    input("▶ Press ENTER after you submit the application...")

    driver.quit()
    return True

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def open_greenhouse_job(url):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service("chromedriver/mac-arm64/126.0.6478.182/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    return driver
