import json
import requests
from bs4 import BeautifulSoup

with open('website.json', 'r') as file:
    data = json.load(file)

for site in data:
    domain = site['name']
    url = f"https://{domain}"
    try:
        response = requests.get(url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")

        span = soup.find("span", {"jsselect": "heading", "jsvalues": ".innerHTML:msg"})
        if span:
            site['social_links'] = "No social links found"
        else:
            social_links = []

            for a_tag in soup.find_all("a"):
                if "facebook" in a_tag.get('href', '').lower() or "facebook" in a_tag.text.lower():
                    social_links.append({"name": "Facebook", "link": a_tag.get('href')})
                elif "instagram" in a_tag.get('href', '').lower() or "instagram" in a_tag.text.lower():
                    social_links.append({"name": "Instagram", "link": a_tag.get('href')})
                elif "twitter" in a_tag.get('href', '').lower() or "twitter" in a_tag.text.lower():
                    social_links.append({"name": "Twitter", "link": a_tag.get('href')})

            site['social_links'] = social_links if social_links else "No social links found"

        with open('website.json', 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        site['social_links'] = f"Error processing {domain}: {e}"
        with open('website.json', 'w') as file:
            json.dump(data, file, indent=4)
