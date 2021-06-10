import requests

url = "https://postman-echo.com/post"

payload = "Hello DevNet!"
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)
# è possibile utilizzare anche un'altra forma
# response = requests.post(url,headers=headers, data=payload)

print(response.status_code)
print(response.text)