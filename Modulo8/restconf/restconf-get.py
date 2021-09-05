import json
import requests
requests.packages.urllib3.disable_warnings()

# Create a variable named api_url and assign it the URL that will access the interface information on the CSR1kv.
api_url = "https://10.99.99.231/restconf/data/ietf-interfaces:interfaces"

# Create a dictionary variable named headers that has keys for Accept and Content-type 
# and assign the keys the value application/yang-data+json.
headers = {
    "Accept": "application/yang-data+json", 
    "Content-type":"application/yang-data+json"
    }

# Create a Python tuple variable named basicauth that has two keys 
# needed for authentication, username and password
basicauth = ("cisco", "cisco")

# Create a variable to send the request and store the JSON response.
resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

# Print the response
print(resp)

# The response JSON is not compatible with Python dictionary and list objects, 
# so it must be converted to Python format. 
# Create a new variable called response_json and assign the variable resp to it. 
# Add the json() method to convert the JSON
response_json = resp.json()

# To prettify the output, edit your print statement to use the json.dumps() function 
# with the “indent” parameter:
print(json.dumps(response_json, indent=4))