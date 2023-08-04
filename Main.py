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

import Automate
import Scroll

# -------------------------------------------------------------------------------------------

# using webdriver to automate webpage (Chrome)  
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions() 
driver = webdriver.Chrome()


global list_items, certificates_section
