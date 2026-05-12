import time

from playwright.sync_api import Page, expect


def test_get_by_placeholder(page: Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    page.get_by_role("button", name="hide").click()
    time.sleep(2)
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()