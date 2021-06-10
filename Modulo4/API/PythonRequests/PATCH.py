import requests

url = "https://postman-echo.com/patch"

payload = "Hello DevNet!"
headers = {}

response = requests.request("PATCH", url, headers=headers, data=payload)
# è possibile utilizzare anche un'altra forma
# response = requests.patch(url, headers=headers, data=payload)

print(response.status_code)
print(response.text)