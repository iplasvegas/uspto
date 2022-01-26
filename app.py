from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

# Feed a list of search numbers from the csv
search_number = [85931937, 86461534]
# Initialize an empty list for us to add dictionaries of values to which will turn into a pandas df later
data_list = []

for trademark_id in search_number:

    # Connect webdriver to chrome and open the website
    browser = webdriver.Chrome(ChromeDriverManager().install())  #executable_path='/Users/kevinjay/projects/gecko/chromedriver.exe')
    browser.get('https://tsdr.uspto.gov/')

    # Find input area and feed the search number
    serial_input = browser.find_element(By.ID, 'searchNumber')
    # Recall 'trademark_id' is the iterable from the for loop above
    serial_input.send_keys(str(trademark_id) + Keys.RETURN)

    wait = WebDriverWait(browser, 20)

    # Expand all sections
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='expand_all expanded']"))).click()


    registration_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Registration Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    application_filing_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Application Filing Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    us_serial_number = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='US Serial Number:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    mark = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Mark:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    # Need Mark Image - I will talk to you about this
    register = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Register:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    # Also need TM5 which is listed under "value" and not "key"
    # status = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Status']//following-sibling::div[1]"))).get_attribute("innerHTML")
    status_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Status Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    publication_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Publication Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    standard_character_claim = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Standard Character Claim:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    for_ = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='For:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    international_classes = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='International Class(es):']//following-sibling::div[1]"))).get_attribute("innerHTML")
    owner_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Owner Name:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    # earliest_date_can_be_filed = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Earliest date §8 can be filed:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    # latest_date_filed_w_fee = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Latest date §8 can be filed without paying additional fee:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    # latest_date_filed_wo_fee = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Latest date §8 can be filed by paying an additional fee:']//following-sibling::div[1]"))).get_attribute("innerHTML")



    data = {
        'registration_date': registration_date.strip(),
        'application_filing_date': application_filing_date.strip(),
        'mark': mark.strip(),
        'register': register.strip(),
        # 'status': status.strip(),
        'status_date': status_date.strip(),
        'publication_date': publication_date.strip(),
        'standard_character_claim': standard_character_claim.strip(),
        'for_': for_.strip(),
        'international_classes': international_classes.strip().replace('\n', ' '),
        'owner_name': owner_name.strip(),
        # 'earliest_date_can_be_filed': earliest_date_can_be_filed.strip(),
        # 'latest_date_filed_w_fee': latest_date_filed_w_fee.strip(),
        # 'latest_date_filed_wo_fee': latest_date_filed_wo_fee.strip(),
    }

    data_list.append(data)

# Convert to pd.df
data_for_csv = pd.DataFrame(data_list)

# Output the csv to the path
data_for_csv.to_csv('outputs.csv', index=False)
