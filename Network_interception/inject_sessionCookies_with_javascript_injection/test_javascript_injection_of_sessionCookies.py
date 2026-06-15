from playwright.sync_api import Playwright
from PythonPlaywright.API_plus_UI_e2e_test_ecommerce.utils.apiBase import ApiUtils
from API_plus_UI_e2e_test_ecommerce.utils.screenshot_util import screenshot_path


def test_javascript_injection_of_sessionCookies(playwright: Playwright):
    api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com/")
    utils = ApiUtils()
    token_value = utils.getToken(api_request_context)
    browser = playwright.chromium.launch(headless=False)
    browser_context = browser.new_context()
    page = browser_context.new_page()
    browser_context.add_init_script(f"""localStorage.   setItem('token', '{token_value}')""")
    page.goto("https://rahulshettyacademy.com/client/")
    page.get_by_role("button", name="ORDERS").click()
    page.screenshot(path=f"{screenshot_path()}/orders.png")
