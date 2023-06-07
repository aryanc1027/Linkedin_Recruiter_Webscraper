from playwright.sync_api import sync_playwright
import re
import spacy
import csv

nlp = spacy.load("en_core_web_sm")

with sync_playwright() as p:  # closes browser once code is finished
    username = 'mangoaryan02@gmail.com'
    password = 'ChickenHello123#()*'
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://www.linkedin.com/home')
    while page.url != 'https://www.linkedin.com/home':
        page.goto('https://www.linkedin.com/home')
        page.wait_for_load_state()
        page.reload()
    page.fill('input#session_key', username)
    page.fill('input#session_password', password)
    page.click('button[type=submit]')
    # login completed

    page.goto(
        'https://www.linkedin.com/search/results/people/?keywords=recruiter&origin=SWITCH_SEARCH_VERTICAL&searchId'
        '=a1fd6ba3-73f4-4f50-bcc2-b719a137b5de&sid=-x6')
    # goes to the recruiter page
    masterNamesDoub = []
    masterJobTitleDoub = []
    masterLocationDoub = []
    masterCompanyDoub = []
    x = 0
    while x != 100:
        text = page.content()
        wordsInText = text.split()
        patternName = r'<span aria-hidden="true">(.*?)</span>'
        matchesName = re.findall(patternName, text)
        namesHTMLUnfiltered = [re.sub(r'<!---->|•|\d\w+|#+', '', match).strip() for match in matchesName if
                               match.strip()]
        namesFiltered = []
        for string in namesHTMLUnfiltered:
            doc = nlp(string)
            for entity in doc.ents:
                if entity.label_ == 'PERSON':
                    namesFiltered.append(entity.text)

        # print(namesFiltered)

        job_title_elements = page.query_selector_all('.entity-result__primary-subtitle.t-14.t-black.t-normal')
        job_titles = [element.inner_text().strip() for element in job_title_elements]
        # print(job_titles)

        location_elements = page.query_selector_all('.entity-result__secondary-subtitle.t-14.t-normal')
        location = [element.inner_text().strip() for element in location_elements]
        # print(location)

        company_elements = page.query_selector_all('p.entity-result__summary')
        company = [element.inner_text().strip() for element in company_elements]
        patternCompany = r'at\s([A-Za-z\s-]+)'

        companyFil = []
        for string in company:
            matches = re.findall(patternCompany, string)
            if matches:
                companyFil.extend(matches)
            else:
                companyFil.append("Look At Profile for More Info")
        # print(companyFil)

        masterNamesDoub.append(namesFiltered)
        masterLocationDoub.append(location)
        masterCompanyDoub.append(companyFil)
        masterJobTitleDoub.append(job_titles)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.click('button[aria-label="Next"]')
        x += 1

    masterNames = [item for sublist in masterNamesDoub for item in sublist]
    masterLocation = [item for sublist in masterLocationDoub for item in sublist]
    masterCompany = [item for sublist in masterCompanyDoub for item in sublist]
    masterJobTitle = [item for sublist in masterJobTitleDoub for item in sublist]

    rows = [masterNames, masterLocation, masterCompany, masterJobTitle]
    filename = 'output.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    # print(masterCompany)
    # print(masterLocation)
    # print(masterNames)
    # print(masterJobTitle)
