import requests

url = "https://postman-echo.com/get/"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
# è possibile utilizzare anche un'altra forma
# response = requests.get(url,headers=headers, data=payload)

print(response.status_code)
if response.status_code == 200:
    print("OK")
else:
    print("Wrong!")

print(response.text)