import requests

def FetchAndSaveToFile(url,path):
    r = requests.get(url)
    with open(path,'w') as f:
        f.write(r.text)
url = "kathmandupost.com"
http = 'https://'
final =http+url
FetchAndSaveToFile(final,'Ktm.html')
