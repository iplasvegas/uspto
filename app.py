from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
# Connect webdriver to chrome
browser = webdriver.Chrome(ChromeDriverManager().install())  #executable_path='/Users/kevinjay/projects/gecko/chromedriver.exe')
browser.get('https://tsdr.uspto.gov/')

serial_input = browser.find_element(By.ID, 'searchNumber')
serial_input.send_keys('85931937' + Keys.RETURN)

registration_date = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Registration Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
application_filing_date = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Application Filing Date:']//following-sibling::div[1]"))).get_attribute("innerHTML")
us_serial_number = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='US Serial Number:']//following-sibling::div[1]"))).get_attribute("innerHTML")

data = {
    'registration_date': registration_date.strip(),
    'application_filing_date': application_filing_date.strip(),
    'us_serial_number': us_serial_number.strip(),
}

# Convert to pd.df
data_for_csv = pd.DataFrame(data, index=[0])

# Output the csv to the path
data_for_csv.to_csv('outputs.csv', index=False)
