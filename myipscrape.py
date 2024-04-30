import requests 
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def get_info():
    options = Options()
    options.add_experimental_option('detach', True)
    s = Service('D:/BeautifulSoup/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)
    
    last_page = 1  # Initialize the last page visited
    for i in range(last_page, 4968):
        driver.get(f'https://myip.ms/browse/sites/{i}/ipID/23.227.38.32/ipIDii/23.227.38.32')
        time.sleep(5)
        
        # Check if the page visit limit has been exceeded
        try:
            captcha_submit_button = driver.find_element(By.CSS_SELECTOR, '#captcha_submit')
            captcha_submit_button.click()
            time.sleep(2)
        except NoSuchElementException:
            pass  

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        td_elements = soup.find_all('td', class_='row_name')
        data = [{'name': td.a.text.strip(), 'link': td.a['href']} for td in td_elements]
        
        try:
            with open('website.json','a') as f:
                json.dump(data, f, indent=0)
                f.write('\n')  # Add a newline to separate data for each URL
        except Exception as e:
            print(f"Error writing data for page {i}: {e}")
        
        if not data:  # If data is empty, close the browser and restart
            driver.quit()
            return i - 1  # Return the last successful page visited

    driver.quit()  # Close the browser
    return last_page  # Return the last page visited

last_page = get_info()
print(f"Last page visited: {last_page}")
