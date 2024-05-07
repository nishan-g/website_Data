import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

# Required options and service and driver declaration
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('--disable-notifications')
s = Service('D:/BeautifulSoup/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)

def extract_facebook_links(file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Initialize a list to store the extracted data
    extracted_data = []

    # Iterate over each website entry
    for website in data:
        # Check if social_links is a list
        if isinstance(website.get("social_links"), list):
            # Initialize a flag to check if Facebook link is found
            facebook_link_found = False
            # Iterate over each social link
            for link in website["social_links"]:
                # Check if the social link is for Facebook
                if link.get("name") == "Facebook":
                    # Add the extracted data to the list
                    extracted_data.append({
                        "name": website["name"],
                        "facebook_link": link["link"]
                    })
                    facebook_link_found = True
                    break
            # If no Facebook link is found, add placeholder text
            if not facebook_link_found:
                extracted_data.append({
                    "name": website["name"],
                    "facebook_link": "No Facebook link"
                })
        else:
            # If social_links is not a list, add placeholder text
            extracted_data.append({
                "name": website["name"],
                "facebook_link": "No Facebook link"
            })

    # Write the extracted data to a new JSON file
    with open('extracted_facebook_links.json', 'w') as f:
        json.dump(extracted_data, f, indent=4)


def extract_emails_from_text(text):
    # Regular expression pattern for matching email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Find all email addresses in the text
    emails = re.findall(email_pattern, text)
    if emails != []:
        return emails
    else:
        return "No email found"
    # Return the list of email addresses
    
def extract_text_from_span_class(url):
    driver.get(url)
    time.sleep(5)
    resp = driver.page_source
    soup = BeautifulSoup(resp,'html.parser')
    details = soup.find_all('div',{'class':'x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xamitd3 xsyo7zv x16hj40l x10b6aqq x1yrsyyn'})
    
    # Convert details to a string
    details_str = str(details)
    
    return extract_emails_from_text(details_str)
        
    


def extract_pageid(url):
    driver.get(url)
    time.sleep(5)
    resp = driver.page_source
    soup = BeautifulSoup(resp, 'html.parser')
    pageid_data = soup.find_all('div', {'class': 'xyamay9 xqmdsaz x1gan7if x1swvt13'})

    # Convert pageid_data to string
    pageid_data_str = str(pageid_data)
    return extract_pageid_from_data(pageid_data_str)


def extract_pageid_from_data(pageid_data_str):
    match = re.search(r'\b\d{15,}\b', pageid_data_str)
    if match:
        return match.group()
    else:
        return "Page ID not found"


def read_facebook_links(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [entry["facebook_link"] for entry in data]


def process_facebook_links(links_list):
    with open('extracted_facebook_links.json', 'r+') as f:
        extracted_data = json.load(f)

        for link in links_list:
            # Check if the link has a trailing slash
            if link.endswith('/'):
                page_id_url = link + 'about_profile_transparency'
            else:
                page_id_url = link + '/about_profile_transparency'

            if link != 'No Facebook link':
                # Extract the page ID and email from the link
                email = extract_text_from_span_class(link)
                page_id = extract_pageid(page_id_url)

                # Find the corresponding entry in the extracted data
                for entry in extracted_data:
                    if entry["facebook_link"] == link:
                        # Update the entry with page ID and email
                        entry["page_id"] = page_id
                        entry["email"] = email
                        break

                # Write the updated data back to the JSON file
                f.seek(0)
                json.dump(extracted_data, f, indent=4)
                f.truncate()

# Example usage
# extract_facebook_links('website.json')
facebook_links = read_facebook_links('extracted_facebook_links.json')
process_facebook_links(facebook_links)


