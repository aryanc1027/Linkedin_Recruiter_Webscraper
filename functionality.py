import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from bs4 import SoupStrainer as strainer
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
from selenium.webdriver.common.action_chains import ActionChains
import spacy
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pyshorteners



# -------------------------------------------------------------------------------------------

# using webdriver to automate webpage (Chrome)   
driver = webdriver.Chrome()
global list_items, certificates_section


def loginInitiate():
    # Opening linkedIn's login page
    driver.get("https://linkedin.com/uas/login")

    time.sleep(4)

    while (driver.current_url == "https://www.linkedin.com/uas/login"):
        # entering email/phone
        user = input('What is your email or phone number?\n')

        # entering password
        passw = input('What is your password?\n')

        # submitting login information
        login(user, passw)

        # checks for invalid login
        if driver.current_url == "https://www.linkedin.com/checkpoint/lg/login-submit":
            print("Invalid Login Credentials. Please Try Again.")
            driver.get("https://linkedin.com/uas/login")
            time.sleep(4)


def login(user, passw):
    username = driver.find_element(By.ID, "username")
    username.send_keys(user)

    password = driver.find_element(By.ID, "password")
    password.send_keys(passw)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(3)


# detects when user closes window (should be last executed method)
def detectClosedWindow():
    while True:
        try:
            _ = driver.window_handles
        except BaseException as e:
            break
        time.sleep(1)


def scrollToBottom():
    start = time.time()

    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000

    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000

        # we will stop the script for 3 seconds so that
        # the data can load
        time.sleep(3)
        # You can change it as per your needs and internet speed

        end = time.time()

        # scroll for 6 seconds
        if round(end - start) > 6:
            break


def scrollLittle():
    start = time.time()

    # will be used in the while loop
    initialScroll = 0
    finalScroll = 500

    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000

        # we will stop the script for 3 seconds so that
        # the data can load
        time.sleep(2)
        # You can change it as per your needs and internet speed

        end = time.time()

        # scroll for 4 seconds
        if round(end - start) > 4:
            break


def recruitmentInitiate():
    # Filtering by specific user-requested company/companies (add multiple companies functionality later)
    userCompany = input('What company are you interested in?\n')

    # Google searching for company's LinkedIn
    driver.get('http://www.google.com')
    search = driver.find_element(By.NAME, 'q')
    search.send_keys(userCompany + ' linkedin')
    search.send_keys(Keys.RETURN)  # hit return after you enter search text

    time.sleep(3)  # sleep for 5 seconds so you can see the results
    # gets all search results and clicks first link
    driver.find_element(By.CLASS_NAME, "iUh30").click()

    # scrolls to bottom to load all elements of webpage
    scrollToBottom()

    curr_url = driver.current_url
    driver.get(curr_url + "people/?keywords=recruitment")

    scrape()


def scrape():
    scrollLittle()

    # getting all urls from page
    links = set()
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    pplHTML = soup.findAll('a', href=re.compile(r'/in/'))

    # filtering to get profile urls
    for link in soup.findAll("a", href=re.compile(r'/in/')):
        if 'href' in link.attrs:
            links.add(link['href'])

    # printing all urls
    print("\n".join(links))
    final_list = []
    for link in links:
        holder = []
        holder = getTheInfo(str(link))
        final_list.append(holder)

    print(final_list)




def getTheInfo(link_for_person):
    import time

    # Click on people
    # pull from HTML <a class="app-aware-link
    # Create a loop to pull however many peoples info
    # should shove everything into a json

    # Profile Link to be scraped
    link = link_for_person
    driver.get(link)

    # pause before scrolling
    SCROLL_PAUSE_TIME = 6

    # Get the scroll height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    # scroll the entire page due to dynamic loading of the webpage we need to load the entire webpage by scrolling
    for i in range(3):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(SCROLL_PAUSE_TIME / 2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*(2/3));")
        time.sleep(SCROLL_PAUSE_TIME / 2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    try:
        # click to expand experience section
        experiences_expand_button = driver.find_element_by_xpath(
            "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']")
        driver.execute_script("arguments[0].click();", experiences_expand_button)

        time.sleep(2)

        # inline-show-more-text__button link
        experiences_show_more_expand_button = driver.find_element_by_xpath(
            "//button[@class='inline-show-more-text__button link']")
        # print(experiences_show_more_expand_button)
        driver.execute_script("arguments[0].click();", experiences_show_more_expand_button)
    except Exception as e:
        # print("experiences_expand_button Exception:", e)
        pass

    try:
        # click to expand skills section
        skills_expand_button = driver.find_element_by_xpath(
            "//button[@class='pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid']")
        driver.execute_script("arguments[0].click();", skills_expand_button)
    except Exception as e:
        # print("skills_expand_button Exception:", e)
        pass

    # use beautiful soup for html parsing
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")

    # BASIC INFO LIST
    basic_info_list = []

    name_div = soup.find('div', {'class': 'mt2 relative'})
    fullname = name_div.find('h1').get_text().strip()
    try:
        first_name, last_name = fullname.split()
    # above statement fails when a person has put their name as firstname, middlename, lastname
    except:
        try:
            first_name, middle_name, last_name = fullname.split()
        except Exception as e:
            first_name = "Unrecognizable"
            last_name = "Unrecognizable"
            pass

    basic_info_list.append(first_name)
    basic_info_list.append(last_name)

    headline_div = soup.find('div', {'class': 'text-body-medium break-words'})
    headline = headline_div.get_text().strip()
    basic_info_list.append(headline)
    type_tiny = pyshorteners.Shortener()
    shorterLink = type_tiny.tinyurl.short(link)
    basic_info_list.append(shorterLink)


    # Experience Section

    experience_section = soup.find_all('div', {'class': 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline'})
    company_names_list = []
    nlp = spacy.load('en_core_web_sm')
    try:
        for company in experience_section:
            company_names_list.append(company.strip().get_text())
        try:
            for span in experience_section:
                raw_text = span.strip()
                doc = nlp(raw_text)

                for ent in doc.ents:
                    if ent.label_ == 'ORG':
                        company_names_list.append(ent.text)
        except:
            pass

    except Exception as e:
        pass


    # TESTING OUTPUTS
    # print("LISTS")
    # print(basic_info_list)
    # print(education_info_list)
    # print(projects_info_list)
    # print(certifications_info_list)
    # print(experience_info_list)
    # print(skills_info_list)
    # print(volunteer_info_list)
    # print(accomplishments_info_list)
    if 2 > len(company_names_list) > 0:
        final_all_lists = [basic_info_list, company_names_list]
    else:
        final_all_lists = basic_info_list
    print(final_all_lists)
    return final_all_lists







loginInitiate()
recruitmentInitiate()
detectClosedWindow()
getTheInfo()
