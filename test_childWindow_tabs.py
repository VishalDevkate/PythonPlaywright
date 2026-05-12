from playwright.sync_api import Page

'''
def test_childWindow_tabs(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")

    with page.expect_popup() as newPage:
        page.locator(
            ".blinkingText[href='https://rahulshettyacademy.com/documents-request']").click()  # got relative css Selector with SelectorsHub plugin
        childPage = newPage.value
        text = childPage.locator(".red").text_content()
        print(text)
        msg = text.split(" ")
        for i in range(len(msg)):
            if msg[i].__contains__("@"):
                email_id = msg[i]
        print(email_id)
        assert email_id == "mentor@rahulshettyacademy.com"

'''
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")

    # Wait for popup
    with page.expect_popup() as popup_info:
        page.click(".blinkingText")  # triggers new tab

    child_page = popup_info.value  # <-- actual Page object
    print("Popup URL:", child_page.url)
    print("Popup text:", child_page.locator(".red").text_content())

    browser.close()

with sync_playwright() as p:
    run(p)

