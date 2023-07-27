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


    
#-------------------------------------------------------------------------------------------

#using webdriver to automate webpage (Chrome)
driver = webdriver.Chrome(r"C:\Users\arnav\Downloads\chromedriver_win32\chromedriver.exe")    

def loginInitiate():
    # Opening linkedIn's login page
    driver.get("https://linkedin.com/uas/login")

    # entering email/phone
    user = input('What is your email or phone number?\n')
    username = driver.find_element(By.ID, "username")
    username.send_keys(user) 

    # entering password
    passw = input('What is your password?\n')
    password = driver.find_element(By.ID, "password")
    password.send_keys(passw)

    # submitting login information
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(7)

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
    # Google searching for company's linkedin
    driver.get('http://www.google.com')
    search = driver.find_element(By.NAME, 'q')
    search.send_keys(userCompany + ' linkedin')
    search.send_keys(Keys.RETURN) # hit return after you enter search text
    time.sleep(3) # sleep for 5 seconds so you can see the results
    # gets all search results and clicks first link
    driver.find_element(By.CLASS_NAME, "iUh30").click()
    # scrolls to bottom to load all elements of webpage
    scrollToBottom()

    curr_url = driver.current_url
    driver.get(curr_url + "people/?keywords=recruitment")


    scrape()

def scrape():
    #GETTING ALL PROFILE URLS
    scrollLittle()
    lnks=driver.find_elements(By.TAG_NAME,"a")
    # traverse list
    linkStrings = []
    for lnk in lnks:
    # get_attribute() to get all href
        linkStrings.append(lnk.get_attribute("href"))

    print(len(linkStrings))
    del linkStrings[0:25]
    del linkStrings[len(linkStrings) - 83:]
    
    linkNews = [link for link in linkStrings if filterLinks(link)]
    #filterLinks2(linkStrings)


def filterLinks(url):

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(cc, 'html.parser')

    # Check if the page contains the LinkedIn profile indicator
    profile_indicator = soup.find('code', attrs={'class': 'top-card-primary-content__title'})
    if profile_indicator:
        return True

    return False


""""
def filterLinks2(urls):
    # Sample list of HTML links

    # Load the spaCy English model
    nlp = spacy.load('en_core_web_sm')
    unique_links = set()

    # Iterate over the HTML links and search for names
    for link in urls:
        doc = nlp(link)
        for token in doc:
            if token.like_url:
                unique_links.add(token.text)
                print(token.text)
"""

    
    
            
    

loginInitiate()
recruitmentInitiate()
detectClosedWindow()