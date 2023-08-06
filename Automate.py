from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import Scroll
import Scrape
import sqlite3
import pandas as pd
from flask import Flask, send_file

# Defining a chrome driver object tp navigate through webpages
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions() 
driver = webdriver.Chrome()

global list_items, certificates_section

# Submitting login info
def login(user, passw):
        username = driver.find_element(By.ID, "username")
        username.send_keys(user)

        password = driver.find_element(By.ID, "password")
        password.send_keys(passw)

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(3)

# Asking for login information and verifying that it is valid
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


# Detects when user closes window, and ends program
def detectClosedWindow():
        while True:
            try:
                _ = driver.window_handles
            except BaseException as e:
                break
            time.sleep(1)

# Filters by specific user-requested company/companies
def filterCompanyLinks():
        userCompany = input('What company are you interested in?\n')

        # Google searching for company's LinkedIn
        driver.get('http://www.google.com')
        search = driver.find_element(By.NAME, 'q')
        search.send_keys(userCompany + ' linkedin')
        search.send_keys(Keys.RETURN) 

        time.sleep(3) 
        
        # Gets all search results and clicks first link
        driver.find_element(By.CLASS_NAME, "iUh30").click()

        # Scrolls to bottom to load all elements of webpage
        Scroll.scrollToBottom(driver)

        curr_url = driver.current_url
        driver.get(curr_url + "people/?keywords=recruitment")

        Scrape.getAllLinks(driver)

loginInitiate()
filterCompanyLinks()
detectClosedWindow()