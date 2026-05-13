import time

from playwright.sync_api import Page, expect
import time

def wait_for_dom_stability(frame, timeout=10000, stable_ms=500):
    """Wait until the iframe DOM stops changing for stable_ms milliseconds."""
    start = time.time()
    last_html = ""
    while (time.time() - start) * 1000 < timeout:
        current_html = frame.locator("body").inner_html()
        if current_html == last_html:
            # DOM hasn't changed since last check
            time.sleep(stable_ms / 1000.0)
            # re-check after stable_ms
            if frame.locator("body").inner_html() == current_html:
                return True
        else:
            last_html = current_html
            time.sleep(0.2)  # small pause before re-check
    raise TimeoutError("DOM did not stabilize within timeout")


def test_frame(page: Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.frame_locator("#courses-iframe").get_by_role("link", name= "All Access plan").click()
    #time.sleep(10)
    expect(page.frame_locator("#courses-iframe").locator("body")).to_contain_text("Happy Subscibers!")
    # Extra wait for content load
    frame = page.frame_locator("#courses-iframe")
    #frame.locator("body").locator("text=Happy Subscibers!").wait_for(state="visible")
    wait_for_dom_stability(frame)

    # Wait until new content appears
    target = frame.locator("text=Happy Subscibers!")
    expect(target).to_be_visible(timeout=10000)

    # Full-page screenshot (entire page, not just viewport)
    page.screenshot(path="./screenshots/full_page.png", full_page=True)
'''
    # Wait until new content appears
    target = frame.locator("text=Happy Subscibers!")
    expect(target).to_be_visible(timeout=10000)

    # Scroll the element into view
    target.scroll_into_view_if_needed()

    # Now take screenshot of the whole page
    page.screenshot(path="./screenshots/test_frame_handling.png")

    # Or take screenshot of just the iframe content
    target.screenshot(path="./screenshots/iframe_content.png")
'''


