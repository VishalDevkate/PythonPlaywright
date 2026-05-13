from pydoc import text

from playwright.sync_api import Page, expect


def test_API_plus_UI_e2e_test_ecommerce(page: Page):
    pass

def test_UI_e2e_test_ecommerce(page: Page):
    page.goto("https://rahulshettyacademy.com/client/")
    page.get_by_placeholder("email@example.com").fill("v.d@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("RahulShetty@2026")
    page.locator("#login").click()

    #expect(page.get_by_role("button", name="  Cart ")).to_be_visible()
    expect(page.get_by_role("button", name=" Add To Cart").nth(1)).to_be_visible()
    items = page.locator(".card")
    print(items.count())
    items.filter(has_text="ZARA COAT 3").locator("button").filter(has_text=" Add To Cart").click()
    page.get_by_role("button", name="   Cart").click()
    page.get_by_role("button", name="Checkout❯").click()
    page.get_by_role("textbox").nth(1).click()
    page.get_by_role("textbox").nth(1).fill("123")
    page.get_by_role("textbox", name="Select Country").click()
    page.get_by_role("textbox", name="Select Country").fill("ind")
    #page.locator(".fa fa-search").filter(has_text=" India").click()
    #expect(page.get_by_role("button", name=" India")).to_be_visible()
    page.wait_for_selector(".ta-results list-group ng-star-inserted", state="visible")
    page.get_by_role("button", name=" India").click()
    page.get_by_text("Place Order").click()
    page.get_by_role("button", name="   ORDERS").click()
    page.get_by_role("rowheader", name="6a04b934965c23b43b1716f7").click()