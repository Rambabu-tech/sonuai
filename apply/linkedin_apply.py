from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def apply_linkedin(job_url, resume_path, cover_letter):

    print("🔵 Starting LinkedIn Apply")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    # Step 1: Login manually
    driver.get("https://www.linkedin.com/login")
    input("👉 Login to LinkedIn manually, then press ENTER...")

    # Step 2: Open job page
    driver.get(job_url)
    time.sleep(5)

    try:
        # Step 3: Click Easy Apply
        easy_apply_btn = driver.find_element(
            By.XPATH,
            "//button[contains(@class,'jobs-apply-button')]"
        )
        easy_apply_btn.click()
        time.sleep(3)

        print("✅ Clicked Easy Apply")

        # Step 4: Upload Resume (if present)
        try:
            upload = driver.find_element(By.XPATH, "//input[@type='file']")
            upload.send_keys(resume_path)
            print("📄 Resume uploaded")
        except:
            print("⚠️ Resume upload not required")

        time.sleep(2)

        # Step 5: Click Next/Submit until done
        while True:
            try:
                submit_btn = driver.find_element(
                    By.XPATH,
                    "//button[contains(., 'Submit application')]"
                )
                submit_btn.click()
                print("🎉 Application Submitted")
                break
            except:
                try:
                    next_btn = driver.find_element(
                        By.XPATH,
                        "//button[contains(., 'Next')]"
                    )
                    next_btn.click()
                    print("➡️ Clicked Next")
                    time.sleep(2)
                except:
                    break

        driver.quit()
        return True

    except Exception as e:
        print("❌ LinkedIn Apply Failed:", e)
        driver.quit()
        return False