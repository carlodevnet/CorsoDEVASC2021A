# Import the XML library. This library provides many handy features for formatting, displaying
# and manipulating xml. In this case we are importing the minidom module from xml.dom
from xml.dom import minidom

# Use 'with" to open the file containing XML
with open('DNAOutput.xml') as file:
    # read the whole file us
    data = minidom.parse(file)

# Access values from the XML getting only the needed tags
items = data.getElementsByTagName('tag')

# display the network device id
for item in items:
    print("Network Device ID: " + item.firstChild.nodeValue)
