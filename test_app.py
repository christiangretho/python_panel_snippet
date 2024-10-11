import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_submit_disable(playwright: Playwright) -> None:
    # navigate to page
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5006/app")

    expect(page.query_selector("#submit-btn-id")).to_be_disabled()

    # submit_button = ".bk-GridBox > div:nth-child(13) > .bk-Row > .bk-panel-models-widgets-Button > .bk-btn-group"
    # # Check to see that the save button is disabled when neither the Title or Ace content is filled
    # snippet_title_text_box = page.get_by_placeholder("Snippet Title")

    # snippet_title_text_box.fill("test_snippet")

    # page.locator(".bk-btn-group")

    # expect(submit_button).to_be_disabled()

    # page.locator(".ace_content").click()

    # page.locator("textarea").fill("print('hello world')")

    # expect(page.locator(submit_button)).to_be_enabled()

    # page.locator(submit_button).click()

    # expect(page.get_by_text("test_snippet")).to_be_visible()

    # ---------------------
    context.close()
    browser.close()


# def test_check_save_disabled(playwright: Playwright):
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://localhost:5006/app")
#     page.query_selector("#show-test_snippet-btn").click()
#     # page.locator("div").filter(has_text=re.compile(r"^print\('hello world'\)$")).nth(
#     #     1
#     # ).click()
#     expect(page.get_by_role("button", name="Update")).to_be_disabled()
#     page.query_selector("#update-snippet-editor").click()
#     page.locator("textarea").fill("print('updated')")
#     expect(page.get_by_role("button", name="Update")).to_be_enabled()

#     # ---------------------
#     context.close()
#     browser.close()


with sync_playwright() as playwright:
    test_submit_disable(playwright)
    # test_check_save_disabled(playwright)
