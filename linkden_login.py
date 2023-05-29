from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:  # closes browser once code is finished
    username = input()
    password = input()
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://www.linkedin.com/home')
    page.fill('input#session_key', username)
    page.fill('input#session_password', password)
    page.click('button[type=submit]')
    # login completed

    page.goto(
        'https://www.linkedin.com/search/results/people/?keywords=recruiter&origin=SWITCH_SEARCH_VERTICAL&searchId'
        '=a1fd6ba3-73f4-4f50-bcc2-b719a137b5de&sid=-x6')
    #gets to the recruiter page

