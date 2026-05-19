import json
from playwright.sync_api import sync_playwright


def run(playwright):
    # Launching in headed mode so you can visually watch it happen
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Track failed requests to prove Use Case 1 works
    failed_image_urls = []
    page.on(
        "requestfailed",
        lambda request: failed_image_urls.append(request.url)
        if any(ext in request.url for ext in [".png", ".jpg", ".jpeg"])
        else None,
    )

    # ------------------------------------------------------------------
    # USE CASE 1: Abort/Block Requests (Images)
    # ------------------------------------------------------------------
    page.route(
        "**/*.{png,jpg,jpeg,svg}", lambda route: route.abort("blockedbyclient")
    )

    # ------------------------------------------------------------------
    # USE CASE 2: Mock an API Response completely (Stubbing Login)
    # ------------------------------------------------------------------
    def mock_login_response(route):
        # We supply a fake token and fake user profile info
        mock_data = {
            "token": "MOCKED_JWT_TOKEN_ABC123",
            "user": {"name": "Test User", "role": "Admin"},
            "userId": "6411a7a1c941646b7a8b3dd1",
            "message": "Login Successfully",
        }
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_data),
        )

    page.route("**/api/ecom/auth/login", mock_login_response)

    # ------------------------------------------------------------------
    # USE CASE 3: Intercept, Inspect, and Modify a Real Response
    # ------------------------------------------------------------------
    def modify_order_response(route):
        # 1. Let the request hit the real server and get the real response
        response = route.fetch()
        try:
            json_body = response.json()

            # 2. Tamper with the real response data before giving it to the browser UI
            if "orders" in json_body:
                # Override the real database order IDs with our custom fake ID
                json_body["orders"] = ["MOCK_ORDER_999"]
                json_body["message"] = "Intercepted and modified!"

            # 3. Feed the tampered payload to the UI
            route.fulfill(response=response, json=json_body)
        except Exception:
            route.continue_()

    page.route("**/api/ecom/order/create-order", modify_order_response)

    # ------------------------------------------------------------------
    # TEST EXECUTION & DEMONSTRATION
    # ------------------------------------------------------------------
    page.goto("https://rahulshettyacademy.com/client/")

    # DEMO 1 VERIFICATION: Check if images are missing alternative placeholders/failed
    print(f"--- Demonstration 1: Image Blocking ---")
    print(f"Blocked Image requests URLS: {failed_image_urls}")
    print(f"Blocked Image Requests Count: {len(failed_image_urls)}")
    assert len(failed_image_urls) > 0, "Failed to block images!"
    print("✅ Verified: Images successfully blocked via interceptor.")

    # DEMO 2 EXECUTION: Trigger Login API Call
    print(f"\n--- Demonstration 2: API Mocking (Login) ---")
    page.get_by_placeholder("email@example.com").fill("v.d@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("RahulShetty@2026")

    # Use expect_response to trap the network transaction while clicking login
    with page.expect_response("**/api/ecom/auth/login") as response_info:
        page.get_by_role("button", name="Login").click()

    login_response = response_info.value
    captured_token = login_response.json()["token"]

    print(f"Captured Login Token from Network: {captured_token}")
    assert (
        captured_token == "MOCKED_JWT_TOKEN_ABC123"
    ), "Login was not mocked!"
    print("✅ Verified: The application accepted our fake Mocked Login Token.")

    # DEMO 3 EXECUTION: Order Placement Modification
    print(f"\n--- Demonstration 3: Response Modification (Orders) ---")

    # Wait for dashboard items to load, then add the first item to cart
    page.locator(".card-body").first.wait_for(state="visible")
    page.locator(".card-body").original_by_text = page.get_by_role(
        "button", name=" Add To Cart"
    ).first.click()

    # Navigate to Cart -> Checkout
    page.get_by_role("button", name="Cart").click()
    page.get_by_role("button", name="Checkout").click()

    # Fill out mandatory country field
    page.get_by_placeholder("Select Country").press_sequentially(
        "ind", delay=100
    )
    page.get_by_role("button", name=" India").click()

    # Trap the create-order request while clicking "Place Order"
    with page.expect_response(
        "**/api/ecom/order/create-order"
    ) as order_response_info:
        page.locator(".action__submit").click()

    # Validate what the UI received vs what it displays
    modified_order_json = order_response_info.value.json()
    print(f"Server Response modified to: {modified_order_json['orders']}")

    # Check the UI text to see if the browser renders our injected fake order number
    ui_confirmation_text = page.locator("label.ng-star-inserted").text_content()
    print(f"UI Displayed Order ID: {ui_confirmation_text}")

    assert (
        "MOCK_ORDER_999" in ui_confirmation_text
    ), "UI did not show the modified Order ID!"
    print(
        "✅ Verified: The backend response was altered, forcing the UI to display 'MOCK_ORDER_999'."
    )

    page.wait_for_timeout(3000)
    browser.close()


with sync_playwright() as playwright:
    run(playwright)