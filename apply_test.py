from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Open demo form
    page.goto("https://www.selenium.dev/selenium/web/web-form.html")

    # Fill text input
    page.fill("input[name='my-text']", "Rambabu Kurva")

    # Fill password
    page.fill("input[name='my-password']", "dummy-password")

    # Select dropdown
    page.select_option("select[name='my-select']", "2")

    # Click submit button
    page.click("button")

    # Wait so you can see result
    page.wait_for_timeout(5000)

    browser.close()
