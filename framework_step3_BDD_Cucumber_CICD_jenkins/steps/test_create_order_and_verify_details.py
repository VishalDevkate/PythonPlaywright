import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from pageObjects.login import loginPage
from utils.apiBase import ApiUtils

scenarios('C:/Users/vdevk/PycharmProjects/PythonPlaywright/framework_step3_BDD_Cucumber_CICD_jenkins/features/createOrder_and_verifyDetails.feature')

@pytest.fixture
def shared_data():
    return {}

@given(parsers.parse('order created through API with {username} and {password}'))
def create_order_through_API(playwright, username, password, shared_data):
    user_credentials = {}
    user_credentials['userEmail'] = username
    user_credentials['userPassword'] = password
    utils = ApiUtils()
    created_order_id = utils.createorder(playwright, user_credentials)
    print("Created order id: ", created_order_id)
    shared_data['created_order_id'] = created_order_id

@when('user is on login page')
def launch_page(browser_instance, shared_data):
    login_page = loginPage(browser_instance)
    shared_data['login_page'] = login_page

@when(parsers.parse('user logs in with {username} and {password}'))
def login(username, password, shared_data):
    login_page = shared_data['login_page']
    dashboard_page = login_page.login(username, password)
    shared_data['dashboard_page'] = dashboard_page

@when('user navigates to orders page')
def navigate_to_orders_page(shared_data):
    dashboard_page =shared_data['dashboard_page']
    # Click on Orders link
    my_orders = dashboard_page.click_orders()
    shared_data['my_orders'] = my_orders

@when('user clicks on latest order')
def click_on_latest_order(shared_data):
    my_orders = shared_data['my_orders']
    # first_order_id
    first_order_id = my_orders.get_latest_order_id()
    shared_data['first_order_id'] = first_order_id
    # View the latest Order details
    order_details = my_orders.get_latest_order_details()
    shared_data['order_details'] = order_details

@then('Thank you for shopping message is displayed')
def verify_thanks_message(shared_data):
    order_details = shared_data['order_details']
    # Verify message on Order summary
    assert order_details.get_message().__eq__("Thank you for Shopping With Us")