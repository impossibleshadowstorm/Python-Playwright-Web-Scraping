import os
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=10)
    page = browser.new_page()
    page.goto("https://solargroup.com/industrial-explosives/#contact")
    page.wait_for_timeout(5000)

    while page.is_visible("body > div.page.page4 > div.pageCenter > div > div.pageContent > div.footer.milestone-footer"):
        page.wait_for_timeout(5000)
        page.screenshot(path='screenshot.png')
        page.keyboard.press("PageDown")
        page.wait_for_timeout(5000)
        page.keyboard.press("PageDown")
        page.wait_for_timeout(5000)
        page.keyboard.press("End")
        page.wait_for_timeout(5000)
        if page.is_visible("body > div.page.page4 > div.pageCenter > div > div.pageContent > div.footer.milestone-footer"):
            page.wait_for_timeout(5000)
            page.screenshot(path='screenshot1.png', full_page=True)
            break
