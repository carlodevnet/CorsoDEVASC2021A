# Author: Stefano Pilla 

# Descrizione: Questo codice è stato creato per la dimostrazione delle API Sincrone
# Utilizza un servizio gratuito raggiungibile a questo indirizzo:
# https://developer.mapquest.com/documentation/

import requests
import json
import os

start = input("Da quale città vuoi partire? ")
arrival = input("In quale città vuoi arrivare? ")

# Define the headers as per Documentation
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Define the API Endpoint URL
api_endpoint = "https://www.mapquestapi.com"

# Define the resource that we would like to use
# in this case the Route
resources = "/directions/v2/route"

# It is also possibile to specifcy the out Format as a param
format = "?outFormat=json"

# It is also possibile to send the API Key as query string
key = "key=2GSkGkWdkAGfABdkAYazQGMg7PaEooAu"

# Create the params 
parameters = f"from={start}&to={arrival}"

# Create the query string with the defined variables values
query = f"{resources}{format}&{key}&{parameters}"

# Print some informative message
print("*" * 30)
print(f"Richiesta in corso utilizzando la seugente query: \n {query}")
print(" ")
print("*" * 30)

# Perform the request and store the response directly in json format
route = requests.get(url=f'{api_endpoint}{query}', headers=headers).json()

# Store the response in a file
base_dir = os.path.dirname(__file__)

# If the directory doesn't exist, let's create it
if not os.path.exists(f"{base_dir}/output/"):
    os.makedirs(f"{base_dir}/output/")

with open(f"{base_dir}/output/directions.json", "w") as file:
    json.dump(route, file, indent=4)

# Select only the maneuvers excluding other info
for maneuvers in route['route']['legs'][0]["maneuvers"]:
    print(maneuvers['narrative'])
