from playwright.sync_api import sync_playwright
import time 

FULL_RIGHT_SCROLL_SELECTOR = (
    '//div[contains(@class, "absolute") and contains(@class, "right-5") and '
    'contains(@class, "top-1/2") and contains(@class, "z-10") and contains(@class, "-translate-y-1/2")]'
    '/button[contains(@class, "-rotate-180")]'
)

FULL_LEFT_SCROLL_SELECTOR = (
    "div.absolute.left-5.top-1\\/2.-translate-y-1\\/2 > button"
)



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1080, 'height': 720})
    page = context.new_page()
    page.goto("https://www.zeptonow.com")

    # Click right scroll button
    page.wait_for_selector(FULL_RIGHT_SCROLL_SELECTOR, timeout=7000)
    btn_right = page.query_selector(FULL_RIGHT_SCROLL_SELECTOR)
    if btn_right:
        btn_right.click()
        
        print("Clicked right scroll button")
        btn_right.click()
        time.sleep(1)
        print("Clicked right scroll button")
        btn_right.click()
        time.sleep(1)
        print("Clicked right scroll button")
        btn_right.click()
        time.sleep(1)
        print("Clicked right scroll button")
        btn_right.click()
        time.sleep(1)
        print("Clicked right scroll button")
        btn_right.click()
        time.sleep(1)
        print("Clicked right scroll button")
        # btn_right.click()
        time.sleep(1)
        print("Clicked right scroll button")
        # btn_right.click()
        time.sleep(1)
    else:
        print("Right scroll button not found")
    time.sleep(10)


    # Click left scroll button
    page.wait_for_selector(FULL_LEFT_SCROLL_SELECTOR, timeout=7000)
    btn_left = page.query_selector(FULL_LEFT_SCROLL_SELECTOR)
    if btn_left:
        btn_left.click()
        time.sleep(1)
        print("Clicked left scroll button")
        btn_left.click()
        time.sleep(1)
        print("Clicked left scroll button")
        btn_left.click()
        time.sleep(1)
        print("Clicked left scroll button")
        btn_left.click()
        time.sleep(1)
        print("Clicked left scroll button")
    else:
        print("Left scroll button not found")

    # ... further actions ...
    browser.close()

