import login
import functionality

login.loginInitiate()
functionality.recruitmentInitiate()

search_results = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead__hit-text')))
    if 'focused' not in search_results.get_attribute('class'):
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead__hit-text'))).click()    

        search_container = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead')))
    if 'focused' not in search_container.get_attribute('class'):
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead button'))).click()


