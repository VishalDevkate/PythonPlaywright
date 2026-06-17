import time
from pathlib import Path

from playwright.sync_api import Page, expect

def screenshot_path():
    # 1. Get the directory where this current test file is saved
    CURRENT_DIR = Path(__file__).resolve().parent

    # 2. Define the exact screenshot target folder (relative to this file)
    SCREENSHOT_DIR = CURRENT_DIR / "screenshots"

    # 3. Create the directory automatically if it doesn't exist yet
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    return SCREENSHOT_DIR

def modify_request(route):
    route.continue_(url="https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=6711e249ae2afd4c0b916fb0")

def test_network_interception_modify_request(page: Page):
    #login
    page.goto("https://rahulshettyacademy.com/client/")
    page.get_by_placeholder("email@example.com").fill("v.d@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("RahulShetty@2026")
    page.locator("#login").click()

    # Click on Orders link
    page.get_by_role("button", name="  ORDERS").click()

    expect(page.get_by_role("row").nth(0)).to_be_visible()
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*", modify_request)
    page.get_by_role("button", name="View").first.click()

    '''
    ordered_product_row = page.get_by_role("row").filter(has_text="6a12c54e17ee3e78ba96c312")
    ordered_product_row.locator("td").locator("button").filter(has_text="View").click()
    '''
    #time.sleep(20)
    page.screenshot(path=f"{screenshot_path()}/modify_request.png")
    message =  page.locator(".blink_me").inner_text()
    assert message == "You are not authorize to view this order"






