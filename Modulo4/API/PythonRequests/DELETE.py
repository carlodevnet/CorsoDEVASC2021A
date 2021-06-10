import requests

url = "https://postman-echo.com/delete"

payload = "Hello DevNet!"

headers = {
  'Content-Type': 'text/plain',
}

response = requests.request("DELETE", url, headers=headers, data=payload)
# è possibile utilizzare anche un'altra forma
# response = requests.delete(url,headers=headers, data=payload)

print(response.status_code)
print(response.text)