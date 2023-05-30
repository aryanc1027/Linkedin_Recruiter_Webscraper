import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

time.sleep(7)

# using webdriver to automate webpage (Chrome)
driver = webdriver.Chrome(r"C:\Users\arnav\Downloads\chromedriver_win32\chromedriver.exe")

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

# detects when user closes window
while True:
    try:
        _ = driver.window_handles
    except BaseException as e:
        break
    time.sleep(1)

    

