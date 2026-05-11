import time

from playwright.sync_api import Page, expect


def test_playwrightbasics(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.rahulshettyacademy.com")
    page.close()

def test_playwrightShortcut(page: Page):
    page.goto("https://www.rahulshettyacademy.com")
    page.close()

def test_coreLocators(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.screenshot(path="./loginpagePractise.png")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.locator("#password").fill("Learning@830$3mK2")   #id is css locator
    #page.get_by_role("radiogroup", name="admin").click()
    page.get_by_role("combobox").select_option("consult")
    page.get_by_role("checkbox", name="terms").check()
    page.get_by_role("button", name="Sign In").click()
    time.sleep(5)
    page.screenshot(path="./loginSuccess.png")

def test_invalidLogin(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.screenshot(path="./loginpagePractise.png")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.locator("#password").fill("Learnisds")   #id is css locator
    #page.get_by_role("radiogroup", name="admin").click()
    page.get_by_role("combobox").select_option("consult")
    page.get_by_role("checkbox", name="terms").check()
    page.get_by_role("button", name="Sign In").click()
    expect(page.get_by_text("Incorrect username/password.")).to_be_visible()
    page.screenshot(path="./loginFailed.png")
