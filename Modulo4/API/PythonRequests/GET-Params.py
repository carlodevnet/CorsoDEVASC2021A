import requests

url = "https://postman-echo.com/get/?test=123"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

# è possibile utilizzare anche un'altra forma
# url = "https://postman-echo.com/get/"
# params = "test=123"
# response = requests.get(url, headers=headers, data=payload, params=params)

print(response.status_code)
print(response.text)