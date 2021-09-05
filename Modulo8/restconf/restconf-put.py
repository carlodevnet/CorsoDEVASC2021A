import json
import requests
requests.packages.urllib3.disable_warnings()

# Create a variable named api_url and assign it the URL that will access the interface information on the CSR1kv.
api_url = "https://10.99.99.231/restconf/data/ietf-interfaces:interfaces/interface=Loopback2"

# Create a dictionary variable named headers that has keys for Accept and Content-type 
# and assign the keys the value application/yang-data+json.
headers = {
    "Accept": "application/yang-data+json", 
    "Content-type":"application/yang-data+json"
    }

# Create a Python tuple variable named basicauth that has two keys 
# needed for authentication, username and password
basicauth = ("cisco", "cisco")


# Create a variable to hold the YANG config that will be applied

yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback2",
        "description": "My second RESTCONF loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.200.200.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}


# Create a variable to send the put request and store the JSON response.
resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

# Print the response
print(resp)

if(resp.status_code >= 200 and resp.status_code <= 299):
    print(f"STATUS OK: {resp.status_code}")
else:
    print(f'Error. Status Code: {resp.status_code} \nError message: {resp.json()}')
