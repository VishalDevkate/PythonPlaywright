from framework_step1.pageObjects.myorders import myOrdersPage


class dashboardPage:
    def __init__(self, page):
        self.page = page

    def click_orders(self):
        self.page.get_by_role("button", name="  ORDERS").click()
        return myOrdersPage(self.page)