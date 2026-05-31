from playwright.sync_api import sync_playwright


def apply_lever(url, resume_path, cover_letter):

    print("🚀 Applying Lever")

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(url, timeout=60000)

            page.click("text=Apply", timeout=5000)

            # Upload resume
            inputs = page.query_selector_all("input[type=file]")
            if inputs:
                inputs[0].set_input_files(resume_path)
                print("✅ Resume uploaded")

            # Basic fields
            try:
                page.fill("input[name='name']", "Rambabu Kurva")
                page.fill("input[name='email']", "rambabukurva899@gmail.com")
            except:
                pass

            page.click("button[type=submit]", timeout=5000)

            print("🎉 Lever success")
            browser.close()
            return True

    except Exception as e:
        print("❌ Lever failed:", e)
        return False