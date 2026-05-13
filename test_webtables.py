from playwright.sync_api import Page, expect
import re


def test_webtables(page: Page):
    #extract and verify the price of Rice
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    #fetching the column number of "Price"
    price_col_number = 0
    for i in range(page.locator("th").count()):
        if page.locator("th").nth(i).text_content().__eq__("Price"):
            price_col_number = i
            print(f'Price column number is {price_col_number}')
            break

    row = page.locator("tr td:text-is('Rice')").locator("..") # go up to the row
    #row = page.locator("tr").filter(has_text=re.compile(r"^Rice$"))   #got error
    #row = page.locator("tr").filter(has=page.locator("td:text('Rice')"))
    #row = page.locator("tr").filter(has_text="Rice").nth(0)    #got error

    cells = row.locator("td")
    print(f'Price of Rice is {cells.nth(price_col_number).inner_text()}')

    """
    riceRow = page.locator("tr").filter(has_text="Rice")
    expect(riceRow.locator("td").nth(price_col_number)).to_have_text("37")
    """
    
