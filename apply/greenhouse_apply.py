import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def apply_greenhouse(job_url, resume_path):

    print("🚀 Applying to Greenhouse:", job_url)

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 15)

    try:
        driver.get(job_url)

        # 🔥 APPLY BUTTON (STRONG LOGIC)
        print("🔍 Searching Apply button...")

        apply_selectors = [
            "//button[contains(., 'Apply')]",
            "//a[contains(., 'Apply')]",
            "//button[contains(., 'Apply Now')]",
            "//a[contains(., 'Apply Now')]",
            "//button[contains(@class,'apply')]",
            "//a[contains(@class,'apply')]"
        ]

        applied = False

        for selector in apply_selectors:
            try:
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Clicked Apply")
                applied = True
                break
            except:
                continue

        if not applied:
            print("❌ Apply button NOT found")
            driver.quit()
            return False

        time.sleep(2)

        # 🔥 HANDLE IFRAME
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                print("✅ Switched to iframe")
                break
            except:
                continue

        time.sleep(2)

        # 🔥 UPLOAD RESUME
        print("📂 Uploading resume...")

        file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")

        uploaded = False
        for inp in file_inputs:
            try:
                inp.send_keys(resume_path)
                uploaded = True
                print("✅ Resume uploaded")
                break
            except:
                continue

        if not uploaded:
            print("⚠️ Resume upload skipped")

        # 🔥 FILL INPUTS
        inputs = driver.find_elements(By.XPATH, "//input")

        for i in inputs:
            try:
                if i.get_attribute("type") in ["text", "email"] and not i.get_attribute("value"):
                    i.send_keys("Rambabu")
            except:
                pass

        print("✍️ Filled fields")

        # 🔥 CHECKBOXES
        checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

        for cb in checkboxes:
            try:
                if not cb.is_selected():
                    driver.execute_script("arguments[0].click();", cb)
            except:
                pass

        print("✅ Checkboxes handled")

        # 🔥 SUBMIT BUTTON
        submit_selectors = [
            "//button[contains(., 'Submit')]",
            "//button[contains(., 'Apply')]",
            "//button[@type='submit']"
        ]

        submitted = False

        for selector in submit_selectors:
            try:
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                driver.execute_script("arguments[0].click();", btn)
                print("🎉 APPLICATION SUBMITTED")
                submitted = True
                break
            except:
                continue

        if not submitted:
            print("⚠️ Submit not found")

        time.sleep(2)
        driver.quit()

        return submitted

    except Exception as e:
        print("❌ Error:", e)
        driver.save_screenshot("error.png")
        driver.quit()
        return False