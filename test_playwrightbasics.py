import time

import pytest
from playwright.sync_api import Page, expect, Playwright


def test_playwrightbasics(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.rahulshettyacademy.com")
    page.close()

def test_playwrightShortcut(page: Page):
    page.goto("https://www.rahulshettyacademy.com")
    page.close()

#below test marked as smoke test. So we can only run smoke tests from command line when needed
#pytest -m smoke
@pytest.mark.smoke
def test_coreLocators(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.screenshot(path="./screenshots/loginpagePractise.png")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.locator("#password").fill("Learning@830$3mK2")   #id is css locator
    #page.get_by_role("radiogroup", name="admin").click()
    page.get_by_role("combobox").select_option("consult")
    page.get_by_role("checkbox", name="terms").check()
    page.get_by_role("button", name="Sign In").click()
    time.sleep(5)
    page.screenshot(path="./screenshots/loginSuccess.png")

def test_invalidLogin(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.screenshot(path="./screenshots/loginpagePractise.png")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.locator("#password").fill("Learnisds")   #id is css locator
    #page.get_by_role("radiogroup", name="admin").click()
    page.get_by_role("combobox").select_option("consult")
    page.get_by_role("checkbox", name="terms").check()
    page.get_by_role("button", name="Sign In").click()
    expect(page.get_by_text("Incorrect username/password.")).to_be_visible()
    page.screenshot(path="./screenshots/loginFailed.png")

def test_firefoxbrowser(playwright: Playwright):
    browser = playwright.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.locator("#password").fill("Learning@830$3mK2")  # id is css locator
    # page.get_by_role("radiogroup", name="admin").click()
    page.get_by_role("combobox").select_option("consult")
    page.get_by_role("checkbox", name="terms").check()
    page.get_by_role("button", name="Sign In").click()
    time.sleep(5)
    page.screenshot(path="./screenshots/loginSuccessFirefoxBrowser.png")
