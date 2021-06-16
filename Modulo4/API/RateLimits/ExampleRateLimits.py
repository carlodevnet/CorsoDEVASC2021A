# Author: Stefano Pilla 

# Descrizione: Questo codice è stato creato per la dimostrazione di come gestire il rate-limiting
# utilizzando la risposta e i parametri restituita dall'API Endpoint

# CREARE UNA VARIABILE D'AMBIENTE CON LA CHIAVE API
# export MERAKI_API_KEY = 'la_tua_chiave_qui'

import requests
import time
import os

# Impostiamo un limite massimo
# In genere questo limite è indicato nella documentazione API
MAX_RETRIES = 20

# Definiziamo una funzione per ottenere tutte le Org 
def get_orgs(MERAKI_API_KEY):
    baseURL = "https://api.meraki.com/api/v1"

    headers = {
        'X-Cisco-Meraki-API-Key': f'{MERAKI_API_KEY}',
        'Content-Type': 'application/json',
        "Accept": 'application/json'
        }

    # Utilizziamo un ciclo for per mantenerci dentro il limite massimo
    for _ in range(MAX_RETRIES):
        # Utilizziamo un try per gestire eventuali eccezioni
        try:
            # Creiamo la richiesta API 
            resp = requests.get(baseURL+'/organizations', headers=headers)
            # Se la risposta è 200 OK allora la richiesta è andata a buon fine
            # Quindi stampa il risultato
            if resp.status_code == 200:
                # Utilizza la funzione print_orgs e passagli come parametro
                # l'oggetto response convertito python dict
                print_orgs(resp.json())
            # Se la risposta è 429 Too many requests
            elif resp.status_code == 429:
                # Stampa un messaggio di errore sulla console
                print("*" * 30)
                print(f'Rate limited - Retrying after {resp.headers["Retry-After"]}.')
                print("*" * 30)
                # Aspettiamo per il tempo indicato nell'header della risposta
                # prima di fare una nuova richiesta
                time.sleep(int(resp.headers['Retry-After']))
                # Allo scadere del tempo, riprova
                continue
            # Altrimenti se il codice è diverso da 200 OK o 429 Too many requests 
            # Stampa i dettagli e esci 
            else:
                raise SystemExit(f'Unexpected status code: {resp.status_code} returned from server.')

        # Se invece c'è un'eccezione allora stampa il messaggio di errore    
        except Exception as e:
            print(e)

# Creiamo una fuzione per stampare le informazioni ottenute dalla request
def print_orgs(orgs):
    for org in orgs:
        print(f"{org['name']} with ID: {org['id']}")
 
if __name__ == "__main__":
    # Leggi la chiave Meraki da una variabile d'ambiente chiamata MERAKI_API_KEY
    API_KEY = os.getenv("MERAKI_API_KEY")

    # Se la variable d'ambiente non è settata mostra un messaggio di errore
    if API_KEY is None:
        print("Please set the MERAKI_API_KEY Env variable (Usage: export MERAKI_API_KEY='YOUR_KEY'")
    # Altrimenti procedi con la richiesta
    else:
        get_orgs(API_KEY)
