# Author: Stefano Pilla 

# Descrizione: Questo codice è stato creato per la dimostrazione delle API Sincrone
# Utilizza un servizio gratuito raggiungibile a questo indirizzo:
# https://deckofcardsapi.com/

# Import requests library to make API Calls
import requests

# This is the deck of cards api endpoint URL
url = "https://deckofcardsapi.com/api/deck/new/shuffle/"

# Let's define some query to be passed to the API request
querystring = {"deck_count": "6"}

# Let's define some headers (not requested by the API in this case)
headers = {
   'Cache-Control': "no-cache",
   }

# Create a request
response = requests.request("GET", url, headers=headers, params=querystring)

# Print the response
print(f"The response is: {response.text}")

# Convert the response in a dict
deck = response.json()

# Get the deck ID and print it
deck_id = deck['deck_id']
print(f"The generated Deck of Card has this ID: {deck_id}")
