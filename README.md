# LinkedIn Web Scraper
This script is a Python program for web scraping LinkedIn to filter company links and retrieve information about people related to the recruitment keyword. It utilizes Selenium for browser automation, BeautifulSoup for parsing web content, and other libraries for various functionalities.

**Prerequisites**
1. Python 3.x is required to run the script.
2. Ensure you have Google Chrome installed on your system, as the script uses Chrome WebDriver for automation.
3. Install the required Python packages by running pip install selenium bs4 spacy requests flask pandas sqlite3.

**Getting Started**
1. Clone or download the script to your local machine.
2. Make sure you have the Chrome WebDriver (chromedriver.exe) placed in the same directory as the script. You can download it from the official website: https://sites.google.com/a/chromium.org/chromedriver/downloads
3. Ensure that you have a valid LinkedIn account to use for scraping.

**How to Use**
1. Open a terminal or command prompt and navigate to the directory containing the script.
2. Run the script using python Automate.py.

**Functionality**
1. Login: The script will prompt you to enter your LinkedIn email or phone number and password. It will then log in to your LinkedIn account.
2. Filter Company Links: The script will ask you to enter the name of a company you are interested in. It will search for the company on Google and navigate to its LinkedIn page. Currently, it searches for people related to the "recruitment" keyword on the company page.
3. Retrieve People Links: The script will extract the links to the profiles of people related to the recruitment keyword and store them in a list. This list is stored in a SQL database, that can then be exported into an Excel file as per the user's command.
4. Detect Closed Window: The script continuously checks if the browser window is closed by the user, and if so, it terminates the script.

**SQL Database Schema**   
employees(  
&ensp; &nbsp; &nbsp;cid INTEGER PRIMARY KEY,  
&ensp; &nbsp; &nbsp;first_name TEXT,  
&ensp; &nbsp; &nbsp;last_name TEXT,  
&ensp; &nbsp; &nbsp;job_title TEXT,  
&ensp; &nbsp; &nbsp;profile_url TEXT);  
