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

serial_input = browser.find_elements(By.ID, 'searchNumber')
serial_input.send_keys('85931937' + Keys.RETURN)

print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Registration Date:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Registration Number:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Application Filing Date:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Mark:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
# Need Mark Image - I will talk to you about this
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Register:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
# Also need TM5 which is listed under "value" and not "key"
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Status']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Status Date:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Publication Date:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Standard Character Claim:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='For:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='International Class(es):']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Owner Name:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Earliest date §8 can be filed:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Latest date §8 can be filed without paying additional fee:']//following-sibling::div[1]"))).get_attribute("innerHTML"))
print(WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key maintenancekey' and text()='Latest date §8 can be filed by paying an additional fee:']//following-sibling::div[1]"))).get_attribute("innerHTML"))



