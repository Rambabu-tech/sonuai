import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def auto_submit_greenhouse(job_url, resume_path, full_name, email):
    try:
        print("🚀 Auto-submitting Greenhouse application...")

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        driver.get(job_url)
        time.sleep(4)

        # Click Apply button if present
        try:
            apply_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Apply')]")
            apply_btn.click()
            time.sleep(3)
        except:
            pass

        # Fill Name
        driver.find_element(By.NAME, "first_name").send_keys(full_name.split()[0])
        driver.find_element(By.NAME, "last_name").send_keys(full_name.split()[-1])

        # Fill Email
        driver.find_element(By.NAME, "email").send_keys(email)

        # Upload Resume
        upload = driver.find_element(By.NAME, "resume")
        upload.send_keys(os.path.abspath(resume_path))

        time.sleep(2)

        # Submit
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()

        print("✅ Application submitted successfully!")

        time.sleep(5)
        driver.quit()

        return True

    except Exception as e:
        print("❌ Auto submit failed:", e)
        return False
