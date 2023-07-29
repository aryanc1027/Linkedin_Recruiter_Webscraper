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
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------------------------------------------------------------------------

# using webdriver to automate webpage (Chrome)   
driver = webdriver.Chrome()


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


def login(user, passw):
    username = driver.find_element(By.ID, "username")
    username.send_keys(user)

    password = driver.find_element(By.ID, "password")
    password.send_keys(passw)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(3)


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

    # Google searching for company's LinkedIn
    driver.get('http://www.google.com')
    search = driver.find_element(By.NAME, 'q')
    search.send_keys(userCompany + ' linkedin')
    search.send_keys(Keys.RETURN)  # hit return after you enter search text

    time.sleep(3)  # sleep for 5 seconds so you can see the results
    # gets all search results and clicks first link
    driver.find_element(By.CLASS_NAME, "iUh30").click()

    # scrolls to bottom to load all elements of webpage
    scrollToBottom()

    curr_url = driver.current_url
    driver.get(curr_url + "people/?keywords=recruitment")

    scrape()


def scrape():
    scrollLittle()

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

    getTheInfo()


def getTheInfo():
    global list_items, certificates_section
    import time

    # Click on people
    # pull from HTML <a class="app-aware-link
    # Create a loop to pull however many peoples info
    # should shove everything into a json

    # Profile Link to be scraped
    link = "https://www.linkedin.com/in/aryanc1027/"
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

    # try to expand sections(if available), else pass
    try:
        # click to expand education section
        education_expand_button = driver.find_element_by_xpath(
            "//section[@id='education-section']//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']")
        driver.execute_script("arguments[0].click();", education_expand_button)
    except Exception as e:
        # print("education_expand_button Exception:", e)
        pass

    try:
        # click to expand projects section
        projects_expand_button = driver.find_element_by_xpath(
            "//div[@class='pv-accomplishments-block__content break-words']//button[@aria-label='Expand projects section' and @aria-expanded='false']")
        driver.execute_script("arguments[0].click();", projects_expand_button)
    except Exception as e:
        # print("projects_expand_button Exception:", e)
        pass

    try:
        # click to expand certifications section
        certifications_expand_button = driver.find_element_by_xpath(
            "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']")
        driver.execute_script("arguments[0].click();", certifications_expand_button)
    except Exception as e:
        # print("certifications_expand_button Exception:", e)
        pass

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

    try:
        # click to expand volunteering section
        volunteer_expand_button = driver.find_element_by_xpath(
            "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']")
        driver.execute_script("arguments[0].click();", volunteer_expand_button)
    except Exception as e:
        # print("volunteer_expand_button Exception:", e)
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
        first_name, middle_name, last_name = fullname.split()

    basic_info_list.append(first_name)
    basic_info_list.append(last_name)

    headline_div = soup.find('div', {'class': 'text-body-medium break-words'})
    headline = headline_div.get_text().strip()
    basic_info_list.append(headline)
    basic_info_list.append(link)

    print(basic_info_list)

    # education section
    education_info_list = []
    try:
        edu_section = soup.find('section', {'id': 'education-section'}).find('ul')
        edu_section = edu_section.find_all('div', {
            'class': 'pv-entity__summary-info pv-entity__summary-info--background-section'})
        college_names = []
        degree_names = []
        field_names = []
        grades = []
        dates = []
        for x in range(len(edu_section)):
            curr_section = edu_section[x]
            try:
                college_name = curr_section.find('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'})
                college_names.append(college_name.get_text())
            except Exception as e:
                # print("Education college_name Exception",e)
                college_names.append('')

            try:
                degree_name = curr_section.find('p', {
                    'class': 'pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal'}).find('span', {
                    'class': 'pv-entity__comma-item'})
                degree_names.append(degree_name.get_text())
            except Exception as e:
                # print("Education degree_name Exception",e)
                degree_names.append('')

            try:
                field_name = curr_section.find('p', {
                    'class': 'pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal'}).find('span', {
                    'class': 'pv-entity__comma-item'})
                field_names.append(field_name.get_text())
            except Exception as e:
                # print("Education field_name Exception",e)
                field_names.append('')

            try:
                grade = curr_section.find('p', {
                    'class': 'pv-entity__secondary-title pv-entity__grade t-14 t-black t-normal'}).find('span', {
                    'class': 'pv-entity__comma-item'})
                grades.append(grade.get_text())
            except Exception as e:
                # print("Education grade Exception",e)
                grades.append('')

            try:
                time = curr_section.find('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'})
                dates.append((time.find_all('time')[1].get_text()))
            except Exception as e:
                # print("Education time Exception",e)
                dates.append('')

        for i in range(len(edu_section)):
            education_info_list.append([college_names[i], degree_names[i], field_names[i], dates[i], grades[i]])
    except Exception as e:
        # no education added
        # print("Education Section Exception", e)
        pass

    print(education_info_list)

    # Project Section
    projects_info_list = []
    project_titles = []
    try:
        project_section = soup.find('div', {'id': 'projects-expandable-content'})
        project_section = project_section.find('ul', {'class': 'pv-accomplishments-block__list'})

        projects = project_section.find_all('h4', {'class': 'pv-accomplishment-entity__title t-14 t-bold'})

        for i in range(len(projects)):
            project_name = projects[i].get_text().split('\n')[2]
            project_name = re.sub(' +', ' ', project_name)
            project_titles.append(project_name.strip())

        projects = project_section.find_all('p', {'class': 'pv-accomplishment-entity__date t-14'})
        project_time = []
        for i in range(len(project_titles)):
            try:
                project_date = projects[i].get_text().split('\n')[1]
                project_date = re.sub(' +', ' ', project_date)
                project_time.append(project_date[1:])
            except Exception as e:
                # print("project_date Exception", e)
                project_time.append('')

        project_descriptions = []
        projects2 = project_section.find_all('p', {'class': 'pv-accomplishment-entity__description t-14'})
        for i in range(len(project_titles)):
            try:
                next_empty_elem = projects2[i].findNext('div')
                curr_proj_desc = next_empty_elem.next_sibling
                project_descriptions.append(curr_proj_desc.strip())
            except Exception as e:
                # print("curr_proj_desc Exception", e)
                project_descriptions.append('')

        # Construct projects_info_list from above data
        for i in range(len(project_titles)):
            projects_info_list.append([project_titles[i], project_time[i], project_descriptions[i]])
    except Exception as e:
        # no projects added
        # print("Project Section Exception", e)
        pass
    print(projects_info_list)

    # certifications section
    certifications_info_list = []
    try:
        certificates_section = soup.find('section', {'id': 'certifications-section'})

        list_items = certificates_section.find('ul',
                                               {
                                                   'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more'})
    except Exception as e:
        # print("certificates_section Exception", e)
        pass
    try:
        if list_items is None:
            list_items = certificates_section.find('ul', {
                'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more'})

        items = list_items.find_all('li',
                                    {'class': 'pv-profile-section__sortable-item pv-certification-entity ember-view'})
        cert_names_list = []
        cert_issuer_list = []
        cert_dates_list = []

        for i in range(len(items)):
            curr_cert_name = items[i].find('h3', {'class': 't-16 t-bold'})
            curr_cert_name = curr_cert_name.get_text().strip()
            cert_names_list.append(curr_cert_name)

            curr_issuer_name = items[i].find_all('p', {'class': 't-14'})[0]
            curr_issuer_name = curr_issuer_name.get_text().strip()
            curr_issuer_name = curr_issuer_name.replace('Issuing authority\n', '')
            cert_issuer_list.append(curr_issuer_name)

            curr_cert_date = items[i].find_all('p', {'class': 't-14'})[1]
            curr_cert_date = curr_cert_date.get_text().strip()
            curr_cert_date = curr_cert_date.replace(
                'Issued date and, if applicable, expiration date of the certification or license\n', '').replace(
                'No Expiration Date', '').replace('Issued ', '')
            cert_dates_list.append(curr_cert_date)

        # adding elements in certifications_info_list as per schema
        for i in range(len(cert_names_list)):
            certifications_info_list.append([cert_names_list[i], cert_dates_list[i], cert_issuer_list[i]])
            print(certifications_info_list)

    except Exception as e:
        # no certificates added
        # print("Certificates Section Exception", e)
        pass



    # Experience Section
    experience_info_list = []
    list_items = []
    items = []

    try:
        experience_section = soup.find('section', {'class': 'experience-section'})
        # print(experience_section)

        list_items = experience_section.find('ul', {
            'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more'})
    except Exception as e:
        # print("experience_section Exception", e)
        pass

    try:
        if list_items is None:
            list_items = experience_section.find('ul',
                                                 {
                                                     'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more'})

        items = list_items.find_all('li', {
            'class': 'pv-entity__position-group-pager pv-profile-section__list-item ember-view'})
        company_names_list = []
        position_list = []
        dates_employed_list = []
        description_list = []

        for i in range(len(items)):
            try:
                curr_name = items[i].find('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'})
                curr_name = curr_name.get_text().strip()
                curr_name = curr_name.split('\n')[0].strip()
                # print("1st currname", curr_name)
                company_names_list.append(curr_name)
            except Exception as e:
                # print("Experience curr_name Exception:", e)
                pass

            try:
                if curr_name is None:
                    curr_name = items[i].find('h3', {'class': 't-16 t-black t-bold'})
                    curr_name = curr_name.get_text().strip()
                    curr_name = curr_name.replace("Company Name\n", '')
                    company_names_list.append(curr_name)
            except Exception as e:
                # print("Experience curr_name Exception:", e)
                pass

            try:
                curr_position = items[i].find('h3', {'class': 't-16 t-black t-bold'})
                curr_position = curr_position.get_text().strip()
                curr_name = curr_name.replace("Company Name\n", '')
                position_list.append(curr_position)
            except Exception as e:
                # print("Experience curr_position Exception:", e)
                pass

            try:
                curr_dates = items[i].find('h4', {'class': 'pv-entity__date-range t-14 t-black--light t-normal'})
                curr_dates = curr_dates.get_text().strip()
                curr_dates = curr_dates.replace('Dates Employed\n', '')
                dates_employed_list.append(curr_dates)
            except Exception as e:
                # print("Experience curr_dates Exception:", e)
                pass

            try:
                curr_description = items[i].find('div',
                                                 {'class': 'pv-entity__extra-details t-14 t-black--light ember-view'})
                curr_description = curr_description.get_text().strip()
                curr_description = curr_description.replace('\n\n\n\n\n        see less', '')
                curr_description = curr_description.replace('\n\n   \n  \n\n\n\n\n\n\n\n\n\n', ' ')
                curr_description = curr_description.replace('\n\n    \n…\n\n        see more', '')
                curr_description = curr_description.replace('\n       ', '.')
                curr_description = curr_description.replace('\n\n', '.')
                description_list.append(curr_description)
            except Exception as e:
                # print("Experience curr_description Exception:", e)
                pass
                # Add empty description for normalization of data
                description_list.append('')

        # create company_names_list from above data
        for i in range(len(company_names_list)):
            experience_info_list.append(
                [company_names_list[i], position_list[i], dates_employed_list[i], description_list[i]])

    except Exception as e:
        # No Experience Added
        # print("Experience Section Exception:", e)
        pass
    print(experience_info_list)

    # Skills Section
    skills_info_list = []
    try:
        skills_section = soup.find('section', {
            'class': 'pv-profile-section pv-skill-categories-section artdeco-container-card ember-view'})
    except Exception as e:
        # print("skills_section Exception", e)
        pass

    try:
        if skills_section is None:
            skills_section = soup.find('section',
                                       {
                                           'class': 'pv-profile-section pv-skill-categories-section artdeco-container-card first-degree ember-view'})

        all_skills = skills_section.find_all('span',
                                             {'class': 'pv-skill-category-entity__name-text t-16 t-black t-bold'})

        for i in range(len(all_skills)):
            skills_info_list.append(all_skills[i].get_text().strip())
            print(skills_info_list)

    except Exception as e:
        # No skills added
        # print("Skills Section Exception:", e)
        pass


    # Volunteering Section:
    volunteer_info_list = []
    items = []
    list_items = []
    try:
        volunteer_section = soup.find('section', {'class': 'pv-profile-section volunteering-section ember-view'})
        list_items = volunteer_section.find('ul', {
            'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more ember-view'})
    except Exception as e:
        # print("Volunteering volunteer_section Exception:", e)
        pass

    try:
        if list_items is None:
            list_items = volunteer_section.find('ul',
                                                {
                                                    'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more'})
    except Exception as e:
        # print("Volunteering list_items Exception:", e)
        pass

    try:
        items = list_items.find_all('li', {
            'class': 'pv-profile-section__sortable-item pv-profile-section__section-info-item relative pv-profile-section__sortable-item--v2 pv-profile-section__list-item sortable-item ember-view'})
    except Exception as e:
        # print("Volunteering list_items Exception:", e)
        pass

    try:
        if items == []:
            items = list_items.find_all('li', {
                'class': 'pv-profile-section__list-item pv-volunteering-entity pv-profile-section__card-item ember-view'})
    except Exception as e:
        # print("Volunteering items Exception:", e)
        pass

    try:
        for i in range(len(items)):
            curr_name = items[i].find('span', {'class': 'pv-entity__secondary-title'})
            curr_name = curr_name.get_text().strip()

            curr_role = items[i].find('h3', {'class': 't-16 t-black t-bold'})
            curr_role = curr_role.get_text().strip()

            try:
                curr_dates = items[i].find('h4', {
                    'class': 'pv-entity__date-range detail-facet inline-block t-14 t-black--light t-normal'})
                curr_dates = curr_dates.get_text().strip()
                curr_dates = curr_dates.replace('Dates volunteered\n', '')
            except Exception as e:
                # print("curr_dates Exception", e)
                curr_dates = ''

            try:
                curr_description = items[i].find('p', {'class': 'pv-entity__description t-14 t-normal mt4'})
                curr_description = curr_description.get_text().strip()
            except Exception as e:
                # print("curr_description Exception", e)
                curr_description = ''

            # Construct volunteer_info_list from above data
            volunteer_info_list.append([curr_name, curr_role, curr_dates, curr_description])

    except Exception as e:
        # no volunteering added
        # print("Volunteering Section Exception", e)
        pass

    try:
        # click to expand honors and awards section because only either projects or honors and awards can be expanded at a time
        honors_and_awards_expand_button = driver.find_element_by_xpath(
            "//section[@class='pv-profile-section pv-accomplishments-section artdeco-container-card ember-view']//button[@aria-label='Expand honors & awards section']")
        driver.execute_script("arguments[0].click();", honors_and_awards_expand_button)

        # click to expand honors and awards section to show more
        honors_and_awards_expand_button2 = driver.find_element_by_xpath(
            "//section[@class='pv-profile-section pv-accomplishments-section artdeco-container-card ember-view']//button[@aria-controls='honors-expandable-content' and @aria-expanded='false']")
        driver.execute_script("arguments[0].click();", honors_and_awards_expand_button2)
    except Exception as e:
        # print("honors_and_awards_expand_button Exception", e)
        pass

    # accomplishments section
    accomplishments_info_list = []
    try:
        accomplishments_section = soup.find_all('section', {
            'class': 'pv-profile-section pv-accomplishments-section artdeco-container-card ember-view'})

        honors_section = accomplishments_section[0].find('div', {'aria-labelledby': 'honors-title'})

        list_items = honors_section.find_all('li', {'class': 'pv-accomplishments-block__summary-list-item'})

        for i in range(len(list_items)):
            accomplishments_info_list.append(list_items[i].get_text().strip())

    except Exception as e:
        # No accomplishments added
        # print("Accomplishments Section Exception", e)
        pass

    # Close the driver once scraping is done
    driver.close()

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

    final_all_lists = [basic_info_list, education_info_list, projects_info_list, certifications_info_list,
                       experience_info_list, skills_info_list,
                       volunteer_info_list, accomplishments_info_list]

    print(final_all_lists)


loginInitiate()
recruitmentInitiate()
detectClosedWindow()
getTheInfo()
