import time

from playwright.sync_api import Page, expect


def test_dialog_alerts(page: Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("#confirmbtn").click()
    #page.get_by_role("button", name="Confirm").click()
    time.sleep(5)