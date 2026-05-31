import asyncio
from playwright.async_api import async_playwright
import os

RESUME_PATH = os.path.abspath("uploads/user_1_Kurva_Rambabu_DevOps_Engineer.docx")

PROFILE = {
    "first_name": "Kurva",
    "last_name": "Rambabu",
    "email": "rambabukurva899@gmail.com",
    "phone": "5716680067",
}

async def semi_auto_apply(job_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Opening job page...")
        await page.goto(job_url)
        await page.wait_for_load_state("networkidle")

        frame = page.frame_locator("iframe#grnhse_iframe")
        await frame.locator("form").wait_for()

        print("Filling basic fields...")

        try:
            await frame.get_by_label("First Name").fill(PROFILE["first_name"])
        except:
            pass

        try:
            await frame.get_by_label("Last Name").fill(PROFILE["last_name"])
        except:
            pass

        try:
            await frame.get_by_label("Email").fill(PROFILE["email"])
        except:
            pass

        try:
            await frame.get_by_label("Phone").fill(PROFILE["phone"])
        except:
            pass

        # Upload resume
        try:
            await frame.locator('input[type="file"]').first.set_input_files(RESUME_PATH)
        except:
            pass

        print("\n✅ Form auto-filled.")
        print("🔎 Please review the browser.")
        print("🛑 Manually click 'Submit Application' when ready.")

        # Keep browser open indefinitely
        await page.wait_for_timeout(300000)  # 5 minutes


if __name__ == "__main__":
    asyncio.run(
        semi_auto_apply(
            "https://stripe.com/jobs/listing/account-executive-platforms-existing-business/7456957/apply"
        )
    )