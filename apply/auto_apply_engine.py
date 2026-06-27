import time
import signal
from playwright.sync_api import sync_playwright


# ============================================
# ⏰ GLOBAL TIMEOUT HANDLER
# ============================================
def timeout_handler(signum, frame):
    raise Exception("⏰ Timeout reached")


# ============================================
# 🚀 MAIN APPLY FUNCTION
# ============================================
def apply_with_playwright(job_url, resume_path, cover_letter=""):

    print("\n" + "=" * 60)
    print(f"🤖 SMART APPLY ENGINE: {job_url}")
    print("=" * 60)

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(90)  # 🔥 max 90 seconds per job

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto(job_url, timeout=60000)
            time.sleep(3)

            # ============================================
            # 🔍 APPLY BUTTON (SMART DETECTION)
            # ============================================
            apply_keywords = ["apply", "apply now", "easy apply", "submit application"]

            clicked = False

            for keyword in apply_keywords:
                try:
                    btn = page.locator(f"text={keyword}").first
                    if btn and btn.is_visible():
                        btn.click()
                        print(f"✅ Clicked: {keyword}")
                        clicked = True
                        time.sleep(2)
                        break
                except:
                    continue

            if not clicked:
                print("⚠️ No Apply button → assuming form already open")

            # ============================================
            # 📂 FILE UPLOAD (ROBUST)
            # ============================================
            try:
                file_inputs = page.locator("input[type='file']")

                if file_inputs.count() > 0:
                    file_inputs.first.set_input_files(resume_path)
                    print("✅ Resume uploaded")
                else:
                    print("⚠️ No file upload field")

            except Exception as e:
                print("⚠️ Resume upload failed:", e)

            # ============================================
            # ✍️ INPUT FILL (SMART AI LOGIC)
            # ============================================
            inputs = page.locator("input")

            for i in range(inputs.count()):
                try:
                    field = inputs.nth(i)
                    name = (field.get_attribute("name") or "").lower()
                    placeholder = (field.get_attribute("placeholder") or "").lower()
                    field_type = field.get_attribute("type")

                    if field.input_value():
                        continue

                    if "email" in name or "email" in placeholder:
                        field.fill("rambabukurva899@gmail.com")

                    elif "phone" in name or "phone" in placeholder:
                        field.fill("5716680067")

                    elif "name" in name:
                        field.fill("Rambabu Kurva")

                    elif field_type == "text":
                        field.fill("N/A")

                except:
                    continue

            print("✍️ Inputs filled")

            # ============================================
            # 📝 TEXTAREAS
            # ============================================
            try:
                areas = page.locator("textarea")

                for i in range(areas.count()):
                    try:
                        area = areas.nth(i)
                        if not area.input_value():
                            area.fill(
                                cover_letter or
                                "I am very interested in this opportunity and believe my experience aligns well."
                            )
                    except:
                        continue

                print("📝 Textareas filled")

            except:
                pass

            # ============================================
            # ☑️ CHECKBOXES
            # ============================================
            try:
                checkboxes = page.locator("input[type='checkbox']")

                for i in range(checkboxes.count()):
                    try:
                        cb = checkboxes.nth(i)
                        if not cb.is_checked():
                            cb.check()
                    except:
                        continue

                print("✅ Checkboxes handled")

            except:
                pass

            # ============================================
            # 🔄 MULTI-STEP FORM HANDLER
            # ============================================
            for step in range(3):  # max 3 steps
                try:
                    next_buttons = ["next", "continue", "review"]

                    for txt in next_buttons:
                        try:
                            btn = page.locator(f"text={txt}").first
                            if btn and btn.is_visible():
                                btn.click()
                                print(f"➡️ Step {step+1}: {txt}")
                                time.sleep(2)
                        except:
                            continue
                except:
                    break

            # ============================================
            # 🚀 FINAL SUBMIT
            # ============================================
            submit_keywords = ["submit", "apply", "finish", "send application"]

            submitted = False

            for keyword in submit_keywords:
                try:
                    btn = page.locator(f"text={keyword}").first
                    if btn and btn.is_visible():
                        btn.click()
                        print("🎉 APPLICATION SUBMITTED")
                        submitted = True
                        break
                except:
                    continue

            if not submitted:
                print("⚠️ Submit not found → manual fallback")
                browser.close()
                return False

            time.sleep(3)
            browser.close()

            signal.alarm(0)
            return True

    except Exception as e:
        print("❌ Playwright error:", e)
        signal.alarm(0)
        return False