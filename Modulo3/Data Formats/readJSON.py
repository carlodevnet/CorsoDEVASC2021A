# Import the JSON library. This library provides many handy features for formatting, displaying
# and manipulating json.
import json

# Use 'with" to open the file containing JSON
with open('DNAOutput.json') as file:
    # read the whole file
    data = json.loads(file.read())

# Access values from the JSON and loop through devices and display the network device id

i = 0
for item in data["response"]:
    print("Network Device ID: " + data["response"][i]["networkDeviceId"])
    i += 1
