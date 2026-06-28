from playwright.sync_api import Playwright, sync_playwright

orderPayload = {"orders": [{"country": "India", "productOrderedId": "6960ea76c941646b7a8b3dd5"}]}

class ApiUtils:
    def getToken(self, request_context, user_credentials):
        response = request_context.post("/api/ecom/auth/login", headers={"Content-Type": "application/json"}, data=user_credentials)
        assert response.ok
        token = response.json()["token"]
        return token


    def createorder(self, playwright: Playwright, user_credentials):
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com/")

        token = self.getToken(api_request_context, user_credentials)

        response = api_request_context.post("/api/ecom/order/create-order",
                                 headers={"Content-Type": "application/json",
                                          "Authorization" : token},
                                 data=orderPayload
                                 )
        resp = response.json()
        print("created Order ID: ", resp["orders"][0])
        return resp["orders"][0]

if __name__ == "__main__":
    utils = ApiUtils()
    with sync_playwright() as playwright:
        utils.createorder(playwright)
