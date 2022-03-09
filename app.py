from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from PIL import Image
import pandas as pd
import xlsxwriter
import re
import datetime
from datetime import datetime
from docx import Document
from icalendar import Calendar, Event


# Feed a list of search numbers from the csv
df = pd.read_csv('serial_nums.csv')
# Initialize an empty list for us to add dictionaries of values to which will turn into a pandas df later
data_list = []

# Create outputs workbook and calendar
workbook = xlsxwriter.Workbook('outputs.xlsx')
worksheet = workbook.add_worksheet()
cal = Calendar()

# set a counter for the column headers
counter = 1

for index,row in df.iterrows():
    serial_number_string = str(row[0])
    # Connect webdriver to chrome and open the website
    try:
        browser = webdriver.Chrome(ChromeDriverManager().install())  #executable_path='/Users/kevinjay/projects/gecko/chromedriver.exe')
        browser.get("https://tsdr.uspto.gov/#caseNumber="+serial_number_string+"&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch")

        wait = WebDriverWait(browser, 10)
    except TimeoutException:
        was_there_error = "yes"

    # Expand all sections
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='expand_all expanded']"))).click()
    except TimeoutException:
        was_there_error = "yes"

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
        us_registration_number = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='US Registration Number:']//following-sibling::div[1]"))).get_attribute("innerHTML")
    except TimeoutException:
            us_registration_number = "N/A"
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
        status = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='key' and text()='Status:']//following-sibling::div[1]"))).get_attribute("innerHTML")
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

    # Grab image
    try:
        img = wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@id='markImage']")))
        src = img.get_attribute('src')
        urllib.request.urlretrieve(src, "images/"+serial_number_string+".png")
    except TimeoutException:
        "images/" + serial_number_string + ".png" == "N/A"

    # Open maintenance tab
    try:
        maintenance_tab = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "MAINTENANCE")))
        maintenance_tab.click()

        date_list = browser.find_elements(By.CSS_SELECTOR, 'div.value.maintenanceValue')

        if len(date_list) == 0:
            declaration = 'N/A'
            declaration_of_incontestability = 'N/A'
            earliest_date_can_be_filed = 'N/A'
            latest_date_filed_wo_fee = 'N/A'
            latest_date_filed_w_fee = 'N/A'
        elif len(date_list) == 1:
            declaration = 'N/A'
            declaration_of_incontestability = 'N/A'
            earliest_date_can_be_filed = 'N/A'
            latest_date_filed_wo_fee = 'N/A'
            latest_date_filed_w_fee = date_list[0].get_attribute('innerHTML').replace('.','')
        elif len(date_list) == 2:
            declaration = 'N/A'
            declaration_of_incontestability = 'N/A'
            earliest_date_can_be_filed = 'N/A'
            latest_date_filed_wo_fee = date_list[0].get_attribute('innerHTML').replace('.','')
            latest_date_filed_w_fee = date_list[1].get_attribute('innerHTML').replace('.','')
        elif len(date_list) == 3:
            declaration = 'N/A'
            declaration_of_incontestability = 'N/A'
            earliest_date_can_be_filed = date_list[0].get_attribute('innerHTML').replace('.','')
            latest_date_filed_wo_fee = date_list[1].get_attribute('innerHTML').replace('.','')
            latest_date_filed_w_fee = date_list[2].get_attribute('innerHTML').replace('.','')
        elif len(date_list) == 4:
            declaration = date_list[0].get_attribute('innerHTML').replace('.','')
            declaration_of_incontestability = 'N/A'
            earliest_date_can_be_filed = date_list[1].get_attribute('innerHTML').replace('.','')
            latest_date_filed_wo_fee = date_list[2].get_attribute('innerHTML').replace('.','')
            latest_date_filed_w_fee = date_list[3].get_attribute('innerHTML').replace('.','')
        elif len(date_list) == 5:
            declaration = date_list[0].get_attribute('innerHTML').replace('.', '')
            declaration_of_incontestability = date_list[1].get_attribute('innerHTML').replace('.', '')
            earliest_date_can_be_filed = date_list[2].get_attribute('innerHTML').replace('.', '')
            latest_date_filed_wo_fee = date_list[3].get_attribute('innerHTML').replace('.', '')
            latest_date_filed_w_fee = date_list[4].get_attribute('innerHTML').replace('.', '')
        else:
            print('RUH ROH RAGGY theres too many dates, check serial number: ' + serial_number_string)
            raise AttributeError
    except TimeoutException:
        declaration = 'N/A'
        earliest_date_can_be_filed = 'N/A'
        latest_date_filed_wo_fee = 'N/A'
        latest_date_filed_w_fee = 'N/A'
        declaration_of_incontestability = 'N/A'


    data = {
        'serial_number': serial_number_string,
        'registration_date': registration_date.strip(),
        'us_registration_number': us_registration_number.strip(),
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
        'earliest_date_can_be_filed': earliest_date_can_be_filed.strip(),
        'latest_date_filed_wo_fee': latest_date_filed_wo_fee.strip(),
        'latest_date_filed_w_fee': latest_date_filed_w_fee.strip(),
        'declaration': declaration.replace('<br>', ' ').replace('\n                            ', '').strip(),
        'declaration_of_incontestability': declaration_of_incontestability.strip(),
    }

    # Write to .ics file
 #   if data['earliest_date_can_be_filed'] is not 'N/A':
 #       event = Event()

        # convert to timestamp
 #       datetime_str = data['earliest_date_can_be_filed']
  #      datetime_object = datetime.strptime(datetime_str, '%b %d, %Y')

   #     event.add = ('summary', data['mark']+': Renewal filing period opens')
    #    event.add = ('dstart', 'datetime_object')
     #   event.add = ('description', 'This is the opening of the renewal period for the mark '+data['mark']+'with registration number '+data['us_registration_number'])
      ## cal.add_component(event)


    print(data)
    data_list.append(data)
    browser.close()

    # Set the column variable names.
    # This is meant to be flexible to accomodate a variable number of column names in the future
    if "images/"+serial_number_string+".png" != "N/A":
        if counter == 1:
            column_names = list(data.keys())
            for column_number, name in enumerate(column_names):
                worksheet.write(0, column_number, name)
            # add image column name
            worksheet.write(0, len(list(data.keys()))+1, 'image')

        # Set the actual data into the columns
        trademark_data = list(data.values())
        for column, trademark in enumerate(trademark_data):
            worksheet.write(counter, column, trademark)
        worksheet.insert_image(counter, len(list(data.keys()))+1, 'images/'+serial_number_string+'.png', {'object_position': 1})

        # Set height of the row so its not awkward and squished
        img = Image.open('images/'+serial_number_string+'.png')
        height = img.height
        worksheet.set_row(counter, height)

        # Increase counter by 1
        counter += 1


workbook.close()

#f = open('trademarks.ics', 'wb')
#f.write(cal.to_ical())
#f.close()