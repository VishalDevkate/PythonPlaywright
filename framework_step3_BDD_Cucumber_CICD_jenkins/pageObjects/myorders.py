from playwright.sync_api import expect

from pageObjects.orderDetails import orderDetailsPage


class myOrdersPage:
    def __init__(self, page):
        self.page = page
        self.rows = None
        self.top_row = None

    def get_no_of_orders_on_page(self):
        expect(self.page.get_by_role("row").nth(0)).to_be_visible()
        self.rows = self.page.get_by_role("row")
        print(f'no of rows in webtable/orders on page: {self.rows.count() - 1}')

    def get_latest_order_id(self):
        # get first row
        self.top_row = self.rows.nth(1)
        #top_row = rows.filter(has_text=created_order_id)
        # Get latest order ID
        first_order_id = self.top_row.locator("th").inner_text()
        # expect(top_row.locator("th").nth(0)).not_to_be_empty()
        # first_order_id = top_row.locator("cell").nth(0).inner_text().strip()
        print(f'Latest order ID in Orders list table: {first_order_id}')
        return first_order_id

    def get_latest_order_details(self):
        view_button = self.top_row.locator("td").locator("button").filter(has_text="View")
        view_button.click()
        return orderDetailsPage(self.page)