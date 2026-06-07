

import time
from playwright.sync_api import Playwright, expect
from pytest_playwright.pytest_playwright import browser, context

from framework_step1.utils.apiBase import ApiUtils


def test_API_plus_UI_e2e_test_ecommerce(playwright: Playwright):
    #1.with API calls, create order
    utils = ApiUtils()
    created_order_id = utils.createorder(playwright)

    #2.with UI automation, verify latest order ID on Orders List and View the respective Order details
    #login
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/client/")
    page.get_by_placeholder("email@example.com").fill("v.d@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("RahulShetty@2026")
    page.locator("#login").click()

    #Click on Orders link
    page.get_by_role("button", name="  ORDERS").click()

    #get rows
    expect(page.get_by_role("row").nth(0)).to_be_visible()
    rows = page.get_by_role("row")
    print(f'no of rows in webtable: {rows.count()-1}')

    #get first row
    #top_row = rows.nth(1)
    top_row = rows.filter(has_text=created_order_id)

    #Get latest order ID
    first_order_id = top_row.locator("th").inner_text()
    #expect(top_row.locator("th").nth(0)).not_to_be_empty()
    #first_order_id = top_row.locator("cell").nth(0).inner_text().strip()
    print(f'Latest order ID in Orders list table: {first_order_id}')
    assert first_order_id.__eq__(created_order_id)

    #View the respective Order details
    view_button = top_row.locator("td").locator("button").filter(has_text="View")
    view_button.click()

    #verify content from order details
    #element has two separate classes: col-text and -main. So you need to chain them together with dots (.col-text.-main)
    expect(page.locator(".col-text.-main")).to_be_visible()
    order_summary_order_id = page.locator(".col-text.-main").inner_text()

    # Or Locate by the primary class, then filter by the secondary class match
    #order_summary_order_id = page.locator(".col-text").filter(has_not=page.locator(":not(.-main)")).inner_text()

    print(f'order ID in order Summary: {order_summary_order_id}')
    assert order_summary_order_id == first_order_id

    #Verify message on Order summary
    expect(page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")

    #verify Product Ordered
    order_summary_product_name = page.locator(".artwork-card-info").locator(".title").inner_text()
    print(f'product name in order Summary: {order_summary_product_name}')
    order_summary_product_price = page.locator(".artwork-card-info").locator(".price").inner_text()
    print(f'product price in order Summary: {order_summary_product_price}')

    # go to Home
    page.locator(".fa.fa-home").click()

    #find out a product price with above product name
    expect(page.locator(".card-body").filter(has_text=order_summary_product_name.strip())).to_be_visible()
    product_price = page.locator(".card-body").filter(has_text=order_summary_product_name.strip()).locator(".text-muted").inner_text()
    print(f'product price on home page: {product_price}')

    assert product_price == order_summary_product_price

    context.close()