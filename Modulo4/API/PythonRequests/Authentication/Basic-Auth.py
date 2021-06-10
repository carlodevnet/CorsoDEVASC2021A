import requests
import base64

url = "https://postman-echo.com/basic-auth"
payload={}

'''
# Metodo 1
'''
headers = {
  'Authorization': 'Basic cG9zdG1hbjpwYXNzd29yZA==',
}
response = requests.request("GET", url, headers=headers, data=payload)

'''
# Metodo 3
headers = {}
userpass = ("postman", "password")
response = requests.get(url, headers=headers, data=payload, auth=userpass)
'''

print(response.status_code)
print(response.text)