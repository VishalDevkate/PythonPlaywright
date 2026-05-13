from playwright.sync_api import Page


def test_mouseHover(page: Page):
    page.goto("https://www.rahulshettyacademy.com/AutomationPractice")
    page.locator("#mousehover").hover()
    #page.wait_for_selector(".mouse-hover-content", state="visible")  #sometimes need to add this step for loading mousehovercontent
    page.screenshot(path="./screenshots/mousehover.png")
    page.get_by_role("link", name="Top").click()