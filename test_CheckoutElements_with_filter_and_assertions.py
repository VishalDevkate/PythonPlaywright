from playwright.sync_api import Page, expect


def test_CheckoutElements_with_filter_and_assertions(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_text("Username:").fill("rahulshettyacademy")
    page.get_by_text("Password:").fill("Learning@830$3mK2")
    page.locator("select").select_option("teach")
    page.get_by_role("checkbox", name="terms").check()
    page.locator("#signInBtn").click()

    iPhoneX = page.locator("app-card").filter(has=page.get_by_text("iphone X"))
    iPhoneX.get_by_role("button").click()

    Nokia_Edge = page.locator("app-card").filter(has_text = "Nokia Edge")
    Nokia_Edge.get_by_role("button").click()

    #page.locator(".nav-link btn btn-primary").click()
    page.get_by_text("Checkout").click()

    #expect(page).toHaveURL("https://rahulshettyacademy.com/angularpractice/shop")
    expect(page.locator(".media")).to_have_count(2)
    #expect(page.locator(".media-body").nth(0)).to_have_text("iphone X")
    expect(page.locator(".media-body").nth(0)).to_contain_text("iphone X")
    expect(page.locator(".media-body").nth(1)).to_contain_text("Nokia Edge")


