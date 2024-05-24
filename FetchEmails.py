import json
import pandas as pd
import os
def extract_emails(json_file):
    with open(json_file,'r',encoding='utf-8') as f:
        data = json.load(f)
    
    emails = []
    for entry in data:
        if 'email' in entry  and entry['email'] not in ['No email found',[]]:
            if isinstance(entry['email'], list):
                for email in entry['email']:
                    emails.append({'name': entry['name'], 'email': email})
            else:
                emails.append({'name': entry['name'], 'email': entry['email']})

    return emails

def append_to_csv(csv_file,data):
    df = pd.DataFrame(data)
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file,index=False,mode='w',header=True)

    else:
        df.to_csv(csv_file,index=False ,mode='a',header=False)

json_files = ['extracted_facebook_links.json','extracted_facebook_links1.json']
csv_file = 'emails.csv'

for json_file in json_files:
    email_data = extract_emails(json_file)
    append_to_csv(csv_file,email_data)