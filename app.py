from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Connect webdriver to chrome
browser = webdriver.Chrome(ChromeDriverManager().install())  #executable_path='/Users/kevinjay/projects/gecko/chromedriver.exe')
browser.get('https://tsdr.uspto.gov/')

serial_input = browser.find_element(By.ID, 'searchNumber')
serial_input.send_keys('85931937' + Keys.RETURN)

print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Registration Date:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
