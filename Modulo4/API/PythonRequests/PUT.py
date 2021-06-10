import requests

url = "https://postman-echo.com/put"

payload = "Hello DevNet!"
headers = {}

response = requests.request("PUT", url, headers=headers, data=payload)
# è possibile utilizzare anche un'altra forma
# response = requests.put(url,headers=headers, data=payload)

print(response.status_code)
print(response.text)
