import re
from pydoc import text

from playwright.sync_api import Page, expect


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
    page.get_by_role("textbox", name="Select Country").press_sequentially("ind", delay=100)
    page.get_by_role("button", name=re.compile(" India")).click()

    '''
    # Filling the field all at once doesnt load the suggesstions, hence timeout error
    page.get_by_role("textbox", name="Select Country").fill("ind")
    country_option = page.get_by_role("button", name=re.compile("India"))
    country_option.wait_for(state="visible")
    country_option.click()
    '''
    
    page.get_by_text("Place Order").click()
    page.get_by_role("button", name="   ORDERS").click()
    page.get_by_role("rowheader", name="6a04b934965c23b43b1716f7").click()