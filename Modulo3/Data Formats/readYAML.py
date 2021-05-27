# Import the YAML library. This library provides many handy features for formatting, displaying
# and manipulating YAML. 
import yaml

# Use 'with" to open the file containing YAML
with open('DNAOutput.yaml') as file:
    # read the whole file 
    data = yaml.load(file, Loader=yaml.FullLoader)

# Access values from the YAML getting only response dictonary
items = data['response']

# Loop through devices and display the network device id
for item in items:
    print("Network Device ID: " + item['tag'])
