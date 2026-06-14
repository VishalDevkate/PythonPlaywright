from pageObjects.dashboard import dashboardPage


class loginPage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("https://rahulshettyacademy.com/client/")

    def login(self, username, password):
        self.page.get_by_placeholder("email@example.com").fill(username)
        self.page.get_by_placeholder("enter your passsword").fill(password)
        self.page.locator("#login").click()
        return dashboardPage(self.page)