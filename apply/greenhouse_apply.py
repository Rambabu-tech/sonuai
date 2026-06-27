import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def apply_greenhouse(job_url, resume_path):

    print("\n" + "=" * 60)
    print(f"🚀 Applying to Greenhouse: {job_url}")
    print("=" * 60)

    for attempt in range(2):  # 🔁 retry logic
        driver = None

        try:
            # ============================================
            # 🚀 BROWSER SETUP
            # ============================================
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

            wait = WebDriverWait(driver, 20)

            driver.get(job_url)
            time.sleep(3)

            # ============================================
            # 🔥 CLICK APPLY BUTTON (OPTIONAL)
            # ============================================
            print("🔍 Checking Apply button...")

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
                    print("✅ Clicked Apply button")
                    applied = True
                    break
                except:
                    continue

            if not applied:
                print("⚠️ No Apply button → form may already be open")

            time.sleep(2)

            # ============================================
            # 🔥 HANDLE IFRAME
            # ============================================
            iframes = driver.find_elements(By.TAG_NAME, "iframe")

            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    print("✅ Switched to iframe")
                    break
                except:
                    continue

            time.sleep(2)

            # ============================================
            # 📂 UPLOAD RESUME (ROBUST)
            # ============================================
            print("📂 Uploading resume...")

            resume_uploaded = False
            abs_path = os.path.abspath(resume_path)

            file_inputs = driver.find_elements(By.XPATH, "//input[contains(@type,'file')]")

            if not file_inputs:
                file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")

            for inp in file_inputs:
                try:
                    inp.send_keys(abs_path)
                    print("✅ Resume uploaded")
                    resume_uploaded = True
                    break
                except Exception as e:
                    print("⚠️ Upload attempt failed:", e)

            if not resume_uploaded:
                print("⚠️ Resume upload skipped")

            # ============================================
            # ✍️ FILL INPUT FIELDS (SMART)
            # ============================================
            inputs = driver.find_elements(By.XPATH, "//input")

            for i in inputs:
                try:
                    if i.get_attribute("value"):
                        continue

                    field_type = i.get_attribute("type")
                    name = (i.get_attribute("name") or "").lower()

                    if field_type == "email":
                        i.send_keys("rambabukurva899@gmail.com")

                    elif "phone" in name:
                        i.send_keys("5716680067")

                    elif field_type == "text":
                        i.send_keys("Rambabu")

                except:
                    continue

            print("✍️ Inputs filled")

            # ============================================
            # 📝 TEXTAREAS
            # ============================================
            textareas = driver.find_elements(By.XPATH, "//textarea")

            for t in textareas:
                try:
                    if not t.get_attribute("value"):
                        t.send_keys("I am very interested in this opportunity.")
                except:
                    continue

            print("📝 Textareas filled")

            # ============================================
            # ☑️ CHECKBOXES
            # ============================================
            checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

            for cb in checkboxes:
                try:
                    if not cb.is_selected():
                        driver.execute_script("arguments[0].click();", cb)
                except:
                    continue

            print("✅ Checkboxes handled")

            # ============================================
            # 🚀 SUBMIT BUTTON (IMPROVED)
            # ============================================
            submit_selectors = [
                "//button[contains(., 'Submit')]",
                "//button[contains(., 'Apply')]",
                "//button[contains(., 'Finish')]",
                "//button[contains(., 'Review')]",
                "//button[contains(., 'Send')]",
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
                print("⚠️ Submit button not found")

            time.sleep(3)

            return submitted

        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed:", e)

        finally:
            try:
                if driver:
                    driver.quit()
            except:
                pass

    print("❌ All attempts failed → fallback needed")
    return False