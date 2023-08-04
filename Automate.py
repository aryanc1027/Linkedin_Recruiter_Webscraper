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

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions() 
driver = webdriver.Chrome()

global list_items, certificates_section


def login(user, passw):
        username = driver.find_element(By.ID, "username")
        username.send_keys(user)

        password = driver.find_element(By.ID, "password")
        password.send_keys(passw)

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(3)

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


    # detects when user closes window (should be last executed method)
def detectClosedWindow():
        while True:
            try:
                _ = driver.window_handles
            except BaseException as e:
                break
            time.sleep(1)


def filterCompanyLinks():
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
        Scroll.scrollToBottom(driver)

        curr_url = driver.current_url
        driver.get(curr_url + "people/?keywords=recruitment")

        Scrape.getAllLinks(driver)

loginInitiate()
detectClosedWindow()
filterCompanyLinks()
detectClosedWindow()