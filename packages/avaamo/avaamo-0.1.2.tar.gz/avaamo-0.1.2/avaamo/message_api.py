import requests
import os

url = "https://c0.avaamo.com/conversations/237d4e461e10f6e1a8e4a524e3d2e968/messages.json"

querystring = {
    "page": "1",
    "per_page": "15"
}


headers = {
    'access-token': os.environ['AVAAMO_ACCESS_TOKEN'],
    'accept': "application/json, text/javascript, */*; q=0.01",
}

response = requests.request("GET", url, headers=headers, params=querystring)
response.raise_for_status()

print(response.text)
