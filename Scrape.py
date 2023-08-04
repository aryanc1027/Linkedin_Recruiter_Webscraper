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

import Scroll

def getAllLinks(driver):
    Scroll.scrollLittle(driver)

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
        holder = getTheInfo(driver, str(link))
        final_list.append(holder)

    print(final_list)

def getTheInfo(driver, link_for_person):
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
    basic_info_list.append(link)


    # Experience Section

    experience_section = soup.find_all('div', {'class': 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline'})
    company_names_list = []
    nlp = spacy.load('en_core_web_sm')
    try:
        for company in experience_section:
            company_names_list.append(company.strip().get_text())


    except Exception as e:
        pass


    # Close the driver once scraping is done
    #driver.close()

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
    if len(company_names_list) < 2:
        final_all_lists = [basic_info_list, company_names_list]
    else:
        final_all_lists = [basic_info_list]
    print(final_all_lists)
    return final_all_lists