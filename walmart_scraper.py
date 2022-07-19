from pkg_resources import run_script
from selenium import webdriver 
from selenium.webdriver.common.by import By # targetting

#chrome
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver-manager
from webdriver_manager.firefox import GeckoDriverManager
import chromedriver_binary

# firefox
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService

import random
import pandas as pd


# walmart site
URL = "https://www.google.com/"
WALMART_URL = "https://www.walmart.ca/browse/personal-care/bath-and-body-care/body-wash-and-shower-gel/21021-6000195305349-6000195309552"

#  setting proxy
# PROXY = "91.188.247.217:8085"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
run_script = True


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))#Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL)

# selenium find_element docs https://selenium-python.readthedocs.io/locating-elements.html
product_data_list = []

def get_product_data():
    # scroll to bottom ()
    # driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;") 
    driver.implicitly_wait(15) # wait 
    driver.get("javascript: window.location.href = '{}'".format(WALMART_URL))
    driver.implicitly_wait(25) # wait 
    product_elements = driver.find_elements(By.CSS_SELECTOR, '[data-automation="product"]')

    for product in product_elements:
        # title, price, product_id
        title = product.find_element(By.CSS_SELECTOR, '[data-automation="name"]').text # IMPORTANT ADD "." AT THE BEGINNING OF X PATH TO SEARCH WITHIN
        price = product.find_element(By.CSS_SELECTOR, '[data-automation="current-price"]').text.replace("$","")
        product_id = product.get_attribute("data-product-id")

        product_data = {
            'title': title,
            'price': price,
            'product_id': product_id,
        }
        product_data_list.append(product_data)
    driver.close()
    # try:
    #     # next button
    #     next_button = product.find_element(By.CSS_SELECTOR, '[data-automation="pagination-next-button"]')
    #     next_button.click()
    #     print("CHECKING NEXT PAGE")
    # except:
    #     print("END OF LIST")
    #     run_script = False
    #     pass

    

# looping thru pages until no next button
# while run_script is True:
#     get_product_data()

get_product_data()

# adding data to CSV
CSV_PATH = "product_data.csv"
data = pd.DataFrame(product_data_list)
data.to_csv(CSV_PATH, index=False, encoding='utf-8')
print(data)
