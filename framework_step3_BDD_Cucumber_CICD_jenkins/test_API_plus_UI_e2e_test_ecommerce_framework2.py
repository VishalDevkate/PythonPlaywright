import json
import os
import time

import pytest
from playwright.sync_api import Playwright, expect

from pageObjects.login import loginPage
from utils.apiBase import ApiUtils

# Always resolve relative to this file’s directory
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "credentials.json")

#json->util->python object->use in test
with open(file_path) as f:
    json_data = json.load(f)
    print("json_data: ", json_data)
    user_credentials_list = json_data['user_credentials']
    print("jason_data['user_credentials'][0]['userEmail']: ", json_data['user_credentials'][0]['userEmail'])

@pytest.mark.parametrize("user_credentials", user_credentials_list)
def test_API_plus_UI_e2e_test_ecommerce(playwright: Playwright, user_credentials, browser_instance) :
    #with API calls, create order
    utils = ApiUtils()
    created_order_id = utils.createorder(playwright, user_credentials)


    login_page = loginPage(browser_instance)
    #login_page.navigate()   #since this is moved to browser_instance fixture
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
