from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

# Feed a list of search numbers from the csv
df = pd.read_csv('serial_nums.csv')
# Initialize an empty list for us to add dictionaries of values to which will turn into a pandas df later
data_list = []

for index,row in df.iterrows():

    # Connect webdriver to chrome and open the website
    browser = webdriver.Chrome(ChromeDriverManager().install())  #executable_path='/Users/kevinjay/projects/gecko/chromedriver.exe')
    browser.get("https://tsdr.uspto.gov/#caseNumber="+str(row[0])+"&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch")

    wait = WebDriverWait(browser, 10)

    # Expand all sections
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='expand_all expanded']"))).click()

    try:
        registration_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Registration Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
        registration_date = registration_date.replace('.','')
    except TimeoutException:
        registration_date = "N/A"
    try:
        application_filing_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Application Filing Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
        application_filing_date = application_filing_date.replace('.','')
    except TimeoutException:
        application_filing_date = "N/A"
    try:
        us_serial_number = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='US Serial Number:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
            us_serial_number = "N/A"
    try:
        mark = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Mark:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
        mark = "N/A"
    # Need Mark Image - I will talk to you about this
    try:
        register = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Register:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
        register = "N/A"
    # Also need TM5 which is listed under "value" and not "key"
    try:
        status = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Status']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
        status = "N/A"
    try:
        status_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Status Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
        status_date =  status_date.replace('.','')
    except TimeoutException:
        status_date = "N/A"
    try:
        publication_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Publication Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
        publication_date = publication_date.replace('.','')
    except TimeoutException:
        publication_date = "N/A"
    try:
        standard_character_claim = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Standard Character Claim:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
        standard_character_claim = "N/A"
    try:
        for_ = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='For:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
        for_ = "N/A"
    try:
        international_classes = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='International Class(es):']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
        international_classes = "N/A"
    try:
        owner_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Owner Name:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
        owner_name = "N/A"
    #try:
    #    earliest_date_can_be_filed = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Earliest date §8 can be filed:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    #    earliest_date_can_be_filed = earliest_date_can_be_filed.replace('.','')
    #except TimeoutException:
    #    earliest_date_can_be_filed = "N/A"
    #try:
    #    latest_date_filed_w_fee = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Latest date §8 can be filed without paying additional fee:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    #    latest_date_filed_w_fee = latest_date_filed_w_fee.replace('.','')
    #except TimeoutException:
    #    latest_date_filed_w_fee = "N/A"
    #try:
    #    latest_date_filed_wo_fee = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Latest date §8 can be filed by paying an additional fee:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    #    latest_date_filed_wo_fee =latest_date_filed_wo_fee.replace('.','')
    #except TimeoutException:
    #    latest_date_filed_wo_fee = "N/A"
    #    if standard_character_claim == 'Yes. The mark consists of standard characters without claim to any particular font style, size, or color.':
    #       mark_image = "N/A"
    #    else:
    #        img = wait.until(EC.visibility_of_element_located((By.XPath, '//div[@id="markImage"]/img')))
    #        src = img.getattribute('src')
    #        urllib.urlretrieve(src, +mark+"_image.png")
    #        mark_image = ""+mark+"_image.png"


    data = {
        'serial_number': str(row[0]),
        'registration_date': registration_date.strip(),
        'application_filing_date': application_filing_date.strip(),
        'mark': mark.strip(),
        'register': register.strip(),
        'status': status.strip(),
        'status_date': status_date.strip(),
        'publication_date': publication_date.strip(),
        'standard_character_claim': standard_character_claim.strip(),
        'for_': for_.strip(),
        'international_classes': international_classes.strip().replace('\n', ' '),
        'owner_name': owner_name.strip(),
        #'earliest_date_can_be_filed': earliest_date_can_be_filed.strip(),
        #'latest_date_filed_w_fee': latest_date_filed_w_fee.strip(),
        #'latest_date_filed_wo_fee': latest_date_filed_wo_fee.strip(),
        #'mark_image': mark_image.strip(),
    }
    print(data)
    data_list.append(data)
    browser.close()

# Convert to pd.df
data_for_excel = pd.DataFrame(data_list)

# Output the excel to the path
data_for_excel.to_excel('outputs.xlsx', index=False)
