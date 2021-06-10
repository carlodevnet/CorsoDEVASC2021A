import requests
import json

url = "https://postman-echo.com/post"

payload = {
    'foo1': 'bar1',
    'foo2': 'bar2'
    }

headers = {}

response = requests.request("POST", url, headers=headers, data=payload)
# è possibile utilizzare anche un'altra forma
# response = requests.post(url,headers=headers, data=payload)

print(response.status_code)
jresp = response.json()

print(json.dumps(jresp, indent=6))