from bs4 import BeautifulSoup
import re
import spacy
import pyshorteners
import sqlite3
import pandas as pd
from flask import Flask, send_file

import Scroll
import app

# Scraping information from various profiles
def getAllLinks(driver):
    Scroll.scrollLittle(driver)

    # Getting all links from page using 'href' tag
    links = set()
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    pplHTML = soup.findAll('a', href=re.compile(r'/in/'))

    # Filtering to get profile urls out of comprehensive list
    for link in soup.findAll("a", href=re.compile(r'/in/')):
        if 'href' in link.attrs:
            links.add(link['href'])

    final_list = []
    for link in links:
        holder = []
        holder = getTheInfo(driver, str(link))
        final_list.append(holder)
    driver.close()

    toDatabase(final_list)


def getTheInfo(driver, link_for_person):
    import time

    # Profile Link to be scraped
    link = link_for_person
    driver.get(link)

    SCROLL_PAUSE_TIME = 6

    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scrolls the entire page due to the dynamic loading of the webpage; we need to load the entire webpage by scrolling
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
        # Click to expand experience section
        experiences_expand_button = driver.find_element_by_xpath(
            "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']")
        driver.execute_script("arguments[0].click();", experiences_expand_button)

        time.sleep(2)

        # inline-show-more-text__button link
        experiences_show_more_expand_button = driver.find_element_by_xpath(
            "//button[@class='inline-show-more-text__button link']")
        driver.execute_script("arguments[0].click();", experiences_show_more_expand_button)
    except Exception as e:
        pass

    try:
        # click to expand skills section
        skills_expand_button = driver.find_element_by_xpath(
            "//button[@class='pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid']")
        driver.execute_script("arguments[0].click();", skills_expand_button)
    except Exception as e:
        pass

    # Use BS4 object for html parsing
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")

    # BASIC INFO LIST
    basic_info_list = []

    name_div = soup.find('div', {'class': 'mt2 relative'})
    fullname = name_div.find('h1').get_text().strip()
    try:
        first_name, last_name = fullname.split()
    # Above statement fails when a person has put more than first and last name
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

    # Scrapes Experience Section
    experience_section = soup.find_all('div', {
        'class': 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline'})
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

    if 2 > len(company_names_list) > 0:
        final_all_lists = [basic_info_list, company_names_list]
    else:
        final_all_lists = basic_info_list
    return final_all_lists


# Exports profile information to SQL Database
def toDatabase(listOfData):
    connection = sqlite3.connect('Recruiter_Information.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        first_name TEXT,
                        last_name TEXT,
                        job_title TEXT,
                        profile_url TEXT
                    )''')

    for infomation in listOfData:
        cursor.execute('INSERT INTO employees (first_name, last_name, job_title, profile_url) VALUES (?, ?, ?, ?)',
                       infomation)

    connection.commit()
    connection.close()
    app.toExcel()
