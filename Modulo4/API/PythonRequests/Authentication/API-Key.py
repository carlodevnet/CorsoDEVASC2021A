import requests
import json

url = "https://api.meraki.com/api/v1/organizations"

payload = {}
headers = {
  'X-Cisco-Meraki-API-Key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.status_code)

rjson = response.json()

print(json.dumps(rjson, indent=2))

for org in rjson:
  print(org['name'])
