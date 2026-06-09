from playwright.sync_api import expect


class orderDetailsPage:
    def __init__(self, page):
        self.page = page

    def get_order_id(self):
        # element has two separate classes: col-text and -main. So you need to chain them together with dots (.col-text.-main)
        expect(self.page.locator(".col-text.-main")).to_be_visible()
        order_summary_order_id = self.page.locator(".col-text.-main").inner_text()

        # Or Locate by the primary class, then filter by the secondary class match
        # order_summary_order_id = page.locator(".col-text").filter(has_not=page.locator(":not(.-main)")).inner_text()

        print(f'order ID in order Summary: {order_summary_order_id}')
        return order_summary_order_id

    def get_message(self):
        msg = self.page.locator(".tagline").inner_text()
        print(f'Message: {msg}')
        return msg
        #expect(self.page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")