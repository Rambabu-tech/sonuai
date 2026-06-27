from apply.greenhouse_apply import apply_greenhouse
from apply.lever_apply import apply_lever
from apply.linkedin_apply import apply_linkedin

# 🔥 SAFE IMPORT (NO CRASH)
try:
    from apply.auto_apply_engine import apply_with_playwright
except:
    apply_with_playwright = None

import webbrowser
import time


def apply_to_job(job_url, resume_path, cover_letter):

    if not job_url:
        print("❌ Empty job URL")
        return "FAILED"

    url = job_url.lower()

    print("\n" + "=" * 60)
    print(f"🚀 APPLYING TO: {job_url}")
    print("=" * 60)

    try:

        # -----------------------------------------
        # 🟢 GREENHOUSE
        # -----------------------------------------
        if "greenhouse.io" in url:
            print("🏢 Platform: Greenhouse")

            try:
                success = apply_greenhouse(job_url, resume_path)

                if success:
                    print("✅ Greenhouse Apply Success")
                    return "APPLIED"

            except Exception as e:
                print("⚠️ Greenhouse direct apply failed:", e)

            return _playwright_fallback(job_url, resume_path, cover_letter)

        # -----------------------------------------
        # 🟡 LEVER
        # -----------------------------------------
        elif "lever.co" in url:
            print("🏢 Platform: Lever")

            try:
                success = apply_lever(job_url, resume_path, cover_letter)

                if success:
                    print("✅ Lever Apply Success")
                    return "APPLIED"

            except Exception as e:
                print("⚠️ Lever direct apply failed:", e)

            return _playwright_fallback(job_url, resume_path, cover_letter)

        # -----------------------------------------
        # 🔵 LINKEDIN
        # -----------------------------------------
        elif "linkedin.com" in url:
            print("🏢 Platform: LinkedIn")

            try:
                apply_linkedin(job_url, resume_path)
                print("✅ LinkedIn Auto Apply Success")
                return "APPLIED"

            except Exception as e:
                print("⚠️ LinkedIn auto failed:", e)

                webbrowser.open(job_url)
                return "MANUAL"

        # -----------------------------------------
        # ⚪ OTHER → SMART APPLY
        # -----------------------------------------
        else:
            print("🌐 Unknown Platform → Smart Apply")

            if apply_with_playwright:
                try:
                    result = apply_with_playwright(
                        job_url,
                        resume_path,
                        cover_letter
                    )

                    if result:
                        print("✅ Smart Apply Success")
                        return "APPLIED"

                except Exception as e:
                    print("⚠️ Playwright error:", e)

            print("⚠️ Manual fallback")
            webbrowser.open(job_url)
            return "MANUAL"

    except Exception as e:
        print("❌ CRITICAL APPLY ERROR:", e)
        return "FAILED"

    finally:
        time.sleep(2)


# -----------------------------------------
# 🔥 PLAYWRIGHT FALLBACK
# -----------------------------------------
def _playwright_fallback(job_url, resume_path, cover_letter):

    if not apply_with_playwright:
        print("⚠️ Playwright not available → manual")
        webbrowser.open(job_url)
        return "MANUAL"

    try:
        result = apply_with_playwright(
            job_url,
            resume_path,
            cover_letter
        )

        if result:
            print("✅ Playwright Apply Success")
            return "APPLIED"

        print("❌ Playwright failed → manual")
        webbrowser.open(job_url)
        return "MANUAL"

    except Exception as e:
        print("❌ Playwright error:", e)
        webbrowser.open(job_url)
        return "MANUAL"