import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


    
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

def recruitmentInitiate():
    # searches recruitment as query in linkedin search bar
    search_text = 'recruitment'
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#global-nav-typeahead input'))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#global-nav-typeahead input'))).send_keys(search_text)

    # submits search query request
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#global-nav-typeahead input'))).send_keys(Keys.ENTER)

    # clicks on "People" Filter
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='People']"))).click()

    # clicks on "Current Company" Filter
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Current company']"))).click()
    
    # Filtering by specific user-requested company/companies (add multiple companies functionality later)
    userCompany = input('What company are you interested in?\n')
    company = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Add a company']")
    company.send_keys(userCompany)
    
    #We gotta send keys to this element (look for element) - IN PROGRESS
    driver.find_element(By.CSS_SELECTOR, "[aria-label='20 suggestions found for query: '" + userCompany + "'. Use up and down keys to navigate']").click()
    company.send_keys(Keys.ARROW_DOWN)
    company.send_keys(Keys.ENTER)
    company.send_keys("potato")


loginInitiate()
recruitmentInitiate()
detectClosedWindow()