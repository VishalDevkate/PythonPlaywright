from pathlib import Path

from playwright.sync_api import Page, expect

def save_screenshot(file_name, page: Page):
    # 1. Get the directory where this current test file is saved
    CURRENT_DIR = Path(__file__).resolve().parent

    # 2. Define the exact screenshot target folder (relative to this file)
    SCREENSHOT_DIR = CURRENT_DIR / "screenshots"

    # 3. Create the directory automatically if it doesn't exist yet
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Define your final screenshot file path
    screenshot_path = SCREENSHOT_DIR / f"{file_name}"

    # Inside your test method, pass the string version of the path to Playwright:
    page.screenshot(path=str(screenshot_path))

def screenshot_path():
    # 1. Get the directory where this current test file is saved
    CURRENT_DIR = Path(__file__).resolve().parent

    # 2. Define the exact screenshot target folder (relative to this file)
    SCREENSHOT_DIR = CURRENT_DIR / "screenshots"

    # 3. Create the directory automatically if it doesn't exist yet
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Define your final screenshot file path
    # screenshot_path = SCREENSHOT_DIR / f"{file_name}"

    return SCREENSHOT_DIR

def test_orders_page_without_interception(page: Page):

    #login
    page.goto("https://rahulshettyacademy.com/client/")
    page.get_by_placeholder("email@example.com").fill("v.d@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("RahulShetty@2026")
    page.locator("#login").click()

    # Click on Orders link
    page.get_by_role("button", name="  ORDERS").click()

    # 1. Wait for the URL to change to the My Orders dashboard
    page.wait_for_url("**/dashboard/myorders")

    # 2. Wait for the network to be completely quiet (loading spinner disappears/API finishes)
    page.wait_for_load_state("networkidle")

    #page.screenshot(path="./Network_interception/modify_response/screenshots/OrdersPage_without_interception.png")
    #save_screenshot("orders_page_without_interception.png", page)
    page.screenshot(path=f"{screenshot_path()}/OrdersPage_without_interception.png")

#Modifying response
fake_payload_response = {"data":[],"message":"No Orders"}
def modify_order_response(route):
    route.fulfill(
        json=fake_payload_response
    )
    # Click on Orders link

def test_orders_page_with_interception(page: Page):

    #login
    page.goto("https://rahulshettyacademy.com/client/")
    page.get_by_placeholder("email@example.com").fill("v.d@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("RahulShetty@2026")
    page.locator("#login").click()

    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*", modify_order_response)
    # Click on Orders link
    page.get_by_role("button", name="  ORDERS").click()

    # 1. Wait for the URL to change to the My Orders dashboard
    page.wait_for_url("**/dashboard/myorders")

    # 2. Wait for the network to be completely quiet (loading spinner disappears/API finishes)
    page.wait_for_load_state("networkidle")

    page.screenshot(path=f"{screenshot_path()}/OrdersPage_with_interception.png")



