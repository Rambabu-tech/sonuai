import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

SUCCESS_KEYWORDS = [
    "thank you for applying",
    "application submitted",
    "we have received your application",
    "thanks for your interest"
]

def wait_for_greenhouse_confirmation(driver, timeout=20):
    """
    Detects Greenhouse success page text after manual submit
    """
    print("🔍 Waiting for Greenhouse confirmation page...")

    end_time = time.time() + timeout

    while time.time() < end_time:
        page_text = driver.page_source.lower()

        for keyword in SUCCESS_KEYWORDS:
            if keyword in page_text:
                print("✅ Greenhouse confirmation detected")
                return True

        time.sleep(1)

    print("⚠️ No confirmation text detected")
    return False
