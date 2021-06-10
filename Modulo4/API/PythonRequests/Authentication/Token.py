import requests

url = "https://webexapis.com/v1/rooms"

payload={}

# Generare il proprio token dal sito https://developer.webex.com
headers = {
  'Authorization': 'Bearer <token_da_inserire_qui>'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.status_code)

rjson = response.json()

#print(json.dumps(rjson, indent=2))

for room in rjson['items']:
  if room['title'] == "Corso DevNet Associate 2021/A":
    print(room['id'])