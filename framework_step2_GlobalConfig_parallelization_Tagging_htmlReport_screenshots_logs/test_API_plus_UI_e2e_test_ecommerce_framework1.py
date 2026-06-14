import json
import time

import pytest
from playwright.sync_api import Playwright, expect
from pytest_playwright.pytest_playwright import browser, context

from pageObjects.login import loginPage
from utils.apiBase import ApiUtils

#json->util->python object->use in test
with open("data/credentials.json") as f:
    json_data = json.load(f)
    print("json_data: ", json_data)
    user_credentials_list = json_data['user_credentials']
    print("jason_data['user_credentials'][0]['userEmail']: ", json_data['user_credentials'][0]['userEmail'])

@pytest.mark.parametrize("user_credentials", user_credentials_list)
def test_API_plus_UI_e2e_test_ecommerce(playwright: Playwright, user_credentials) :
    #1.with API calls, create order
    utils = ApiUtils()
    created_order_id = utils.createorder(playwright, user_credentials)

    #2.with UI automation, verify latest order ID on Orders List and View the respective Order details
    #login
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login_page = loginPage(page)
    login_page.navigate()
    dashboard_page = login_page.login(user_credentials['userEmail'], user_credentials['userPassword'])

    #Click on Orders link
    my_orders = dashboard_page.click_orders()

    #get rows
    my_orders.get_no_of_orders_on_page()

    first_order_id = my_orders.get_latest_order_id()
    assert first_order_id.__eq__(created_order_id)

    #View the latest Order details
    order_details = my_orders.get_latest_order_details()

    #verify content from order details
    order_summary_order_id = order_details.get_order_id()
    assert order_summary_order_id == first_order_id

    #Verify message on Order summary
    assert order_details.get_message().__eq__("Thank you for Shopping With Us")

    #verify Product Ordered
    order_summary_product_name, order_summary_product_price = order_details.get_ordered_product_details()

    # go to Home
    dashboard_page = order_details.click_Home()

    #find out a product price with above product name
    product_price = dashboard_page.get_product_details(order_summary_product_name)

    assert product_price == order_summary_product_price

    context.close()