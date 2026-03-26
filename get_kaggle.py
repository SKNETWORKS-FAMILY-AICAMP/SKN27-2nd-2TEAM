import urllib.request
import re

url = 'https://www.kaggle.com/datasets/rhythmghai/netflix-user-watching-behavior-dataset'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'"name":"([a-zA-Z0-9_ ]+)"(?=.*?,"type":"(numeric|string|boolean|datetime|categorical)")', html)
    if matches:
        for match in matches:
            print(match)
    else:
        # Just find any columns metadata
        match = re.search(r'"columns":\[(.*?)\]', html)
        if match:
            print(match.group(1)[:500])
        else:
            print("Not found")
except Exception as e:
    print(e)
