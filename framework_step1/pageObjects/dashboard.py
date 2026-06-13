from playwright.sync_api import expect

from pageObjects.myorders import myOrdersPage


class dashboardPage:
    def __init__(self, page):
        self.page = page

    def click_orders(self):
        self.page.get_by_role("button", name="  ORDERS").click()
        return myOrdersPage(self.page)

    def get_product_details(self, order_summary_product_name):
        expect(self.page.locator(".card-body").filter(has_text=order_summary_product_name.strip())).to_be_visible()
        product_price = self.page.locator(".card-body").filter(has_text=order_summary_product_name.strip()).locator(
            ".text-muted").inner_text()
        print(f'product price on home page: {product_price}')
        return product_price