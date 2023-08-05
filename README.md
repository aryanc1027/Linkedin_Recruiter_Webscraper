# Summer_Project_1
This script is a Python program for web scraping LinkedIn to filter company links and retrieve information about people related to the recruitment keyword. It utilizes Selenium for browser automation, BeautifulSoup for parsing web content, and other libraries for various functionalities.

Prerequisites
Python 3.x is required to run the script.
Ensure you have Google Chrome installed on your system, as the script uses Chrome WebDriver for automation.
Install the required Python packages by running pip install selenium bs4 spacy requests.

Getting Started
Clone or download the script to your local machine.
Make sure you have the Chrome WebDriver (chromedriver.exe) placed in the same directory as the script. You can download it from the official website: https://sites.google.com/a/chromium.org/chromedriver/downloads
Ensure that you have a valid LinkedIn account to use for scraping.

How to Use
Open a terminal or command prompt and navigate to the directory containing the script.
Run the script using python script_name.py.

Functionality
Login: The script will prompt you to enter your LinkedIn email or phone number and password. It will then log in to your LinkedIn account.
Filter Company Links: The script will ask you to enter the name of a company you are interested in. It will search for the company on Google and navigate to its LinkedIn page. Currently, it searches for people related to the "recruitment" keyword on the company page.
Retrieve People Links: The script will extract the links to the profiles of people related to the recruitment keyword and store them in a list.
Detect Closed Window: The script continuously checks if the browser window is closed by the user, and if so, it terminates the script.
