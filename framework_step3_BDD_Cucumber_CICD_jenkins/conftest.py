import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def user_credentials(request):
    print("executing user_credentials fixture from conftext.py")
    return request.param

def pytest_addoption(parser):
    # Check if the option is already added to prevent the ValueError. I think it is considering the browser_name added from framework_step2, so giving value error without below check.
    if not any(opt.dest == "browser_name" for opt in parser._anonymous.options):
        parser.addoption(
            "--browser_name", action="store", default="chrome", help="browser type")
        parser.addoption(
            "--url_name", action="store", default="https://rahulshettyacademy.com/client/", help="page url")

@pytest.fixture(scope="function")  #need not specify scope, since the default scope is function
def browser_instance(playwright: Playwright, request):
    # launch browser from parameter of command line argument
    # pytest --browser_name firefox
    browser_name = request.config.getoption("browser_name")
    url_name = request.config.getoption("url_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()
    #pass url_name from command line
    #pytest --url_name https://rahulshettyacademy.com/client/#/dashboard/dash
    #pytest --url_name https://rahulshettyacademy.com/client/#/dashboard/dash --browser_name firefox
    page.goto(url_name)
    yield page
    context.close()
    browser.close()