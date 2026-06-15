import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def user_credentials(request):
    print("executing user_credentials fixture from conftext.py")
    return request.param

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser type")

@pytest.fixture(scope="function")
def browser_instance(playwright: Playwright, request):
    # launch browser from parameter of command line argument
    # pytest --browser_name firefox
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()