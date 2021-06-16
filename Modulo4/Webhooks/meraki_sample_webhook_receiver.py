# Author: Stefano Pilla 

# Descrizione: Questo codice è stato creato per la dimostrazione dei webhook
# Utilizza due servizi Cisco (Meraki e Webex) con l'ausilio del web framework Flask

# Libraries
from pprint import pprint
from flask import Flask, json, request, render_template
import sys, json
from requests.api import delete
from webexteamssdk import WebexTeamsAPI
import requests
import time

# Importa il file env_user dove sono definite le variabili
import env_user  # noqa

# Definiamo una variable che utilizzeremo successivamente per la
# gestione dell'API Rate Limit
MAX_RETRIES = 20

# Stampiamo le variabili per verificare che siano tutte corrette
# In un ambiente di produzione non è assolutamente consigliato 
# fare questo passaggio
print("WT_ACCESS_TOKEN: " + env_user.WT_ACCESS_TOKEN)
print("WT_ROOM_ID: " + env_user.WT_ROOM_ID)
print("MERAKI API KEY: " + env_user.MERAKI_API_KEY)
print("MERAKI Network: " + env_user.MERAKI_NETWORK)
print("MERAKI Org: " + env_user.MERAKI_ORG)
print("WEBHOOK SECRET: " + env_user.WEBHOOK_SECRET)
print("WEBHOOK URL: " + env_user.WEBHOOK_URL)
print("WEBHOOK SERVER NAME: " + env_user.WEBHOOK_SERVER_NAME)

# WEBEX TEAMS LIBRARY - Utilizziamo l'SDK
teamsapi = WebexTeamsAPI(access_token=env_user.WT_ACCESS_TOKEN)

# Definiamo il base url per meraki 
base_url = "https://api.meraki.com/api/v1"

# Definiamo l'header per le richieste Meraki
headers = {
        "X-Cisco-Meraki-API-Key": env_user.MERAKI_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
        }

# Creiamo un'applicazione Flask
app = Flask(__name__)

# Webhook Receiver Code
# Accetta una post in JSON da Meraki e 
# invia un messaggio in Webex Teams 
@app.route("/", methods=["POST"])
def get_webhook_json():
    global webhook_data

    # Leggiamo i dati della richiesta
    webhook_data = request.json

    # Utilizziamo questa funzione print per verificare la risposta
    # Solo in caso di troubleshooting
    # pprint(webhook_data, indent=1)

    # Definiamo le variabili da voler utilizzare all'interno del messaggio
    deviceSerial = webhook_data['deviceSerial'] 
    deviceModel = webhook_data['deviceModel']
    alertType = webhook_data['alertType']
    alertLevel = webhook_data['alertLevel']
    occureAt = webhook_data['occurredAt']

    # Trasformiamo i dati in JSON
    webhook_data = json.dumps(webhook_data)

    # Webex teams non gestisce più di 1000 caratteri
    # quindi tronchiamo il messaggio
    webhook_data = webhook_data[:1000] + '...'

    # Inviamo il messaggio in webex teams
    teamsapi.messages.create(
        env_user.WT_ROOM_ID,
        markdown=f"## Meraki Webhook Alert: \n Alle ore **{occureAt}** il dispositivo **{deviceSerial}** (Modello: **{deviceModel}**) \n ha generato il seuguente messaggio **{alertType}** - con livello **{str(alertLevel).upper}**")

    # Stampa un messaggio di conferma
    return "WebHook POST Received"

# TEST - Decoratore per creare un API Endpoint all'indirizzo "/"
# In questo caso l'API supporterà solo una GET
@app.route("/", methods=["GET"])
def get_method():
    return "GET ricevuta! L'endpoint API funziona correttamente!"

# TEST - Decoratore per creare un API Endpoint all'indirizzo "/test"
# In questo caso l'API supporterà solo una GET
@app.route("/test", methods=["GET"])
def get_method_test():
    return "URL /test correttamente implementato e funzionante"


# Creiamo un helper per gestire le richieste API
def _req(resource, method="get", auth=None, jsonbody=None, params=None, raise_for_status=True, verify=False):
    # Utilizziamo un ciclo for per mantenerci dentro il limite massimo
    for _ in range(MAX_RETRIES):
        try:
            # Esegue una request generica in base ai valori ottenuti come argomenti
            resp = requests.request(
                method=method, url=f"{base_url}/{resource}", auth=auth, headers=headers, json=jsonbody, params=params, verify=verify)

            # In caso di problemi decommentare per verificare i messaggi
            # print(resp.status_code)
            # print(resp.text)

            # Se la risposta è 200 oppure 204 oppure 201
            if resp.status_code == 200 or resp.status_code == 204 or resp.status_code == 201:
                # Ritorna l'oggetto risp                
                return resp

            # Se la risposta è 429 Too many requests
            elif resp.status_code == 429:
                # print(resp.headers)
                # print(resp.text)
                # Stampa un messaggio di errore sulla console
                print("*" * 30)
                print('Rate limited - Retrying in 5 seconds.')
                print("*" * 30)
                # Aspettiamo per 5 secondi prima di fare una nuova richiesta
                time.sleep(5)
                # Allo scadere del tempo, riprova
                continue
            # Altrimenti se il codice è diverso da 200, 204, 201 o 429  
            # Stampa i dettagli e esci 
            else:
                raise SystemExit(f'Unexpected status code: {resp.status_code} returned from server.')

        # Se invece c'è un'eccezione allora stampa il messaggio di errore    
        except Exception as e:
            resp.raise_for_status()
            print(e)

    # Se raise_for_status variable == True allora stampa l'errore 
    if raise_for_status:
        resp.raise_for_status()


# Elimina eventuali webhook già creati in Meraki
def clear_webhooks(network_id):
    print(f"Deleting webhooks in the Meraki Network with id {network_id}...")

    # Otteniamo i webhook dalla dashboard Meraki
    webhooks = _req(f"/networks/{network_id}/webhooks/httpServers", method="GET", verify=True)
    
    # print(getWebhooks.json())
    # Iteriamo attraverso i webhook e cancelliamoli tutti
    for wk in webhooks.json():
        response = _req(f"/networks/{network_id}/webhooks/httpServers/{wk['id']}", method="delete", verify=True)
        if response.status_code == 204:
            print(f"Webhook {wk['name']} deleted!")
        else:
            print(f"ERROR: {response.text}")


# Otteniamo la Network ID passando come parametro il nome della rete
def get_network_id(network_wh):
    orgs = ""
    print(f"Getting Network ID for network: {network_wh}...")
    # Otteniamo le orgs a cui l'utenza utilizzata ha accesso
    try:
        response = _req("organizations", verify=True)

        # Se lo status_code nella risposta è 200
        # deserializziamo la risposta in un dizionario Python 
        # in modo da poterci lavorare
        if response.status_code == 200:
            orgs = json.loads(response.text)
            # print(json.dumps(orgs, indent=3))
        else:
           # Altrimenti, stampa l'errore 
            print(orgs.text)

    except Exception as e:
        pprint(e)

    # Cerchiamo una rete specifica in base al valore delle variabili d'ambiente
    networks = ""
    print(f"Checking availables Networks in the Org...")
    # Se la lista delle org non è vuota
    if orgs != "":
        # Scorri la lista delle organizzazioni 
        for org in orgs:
            # print(f"ORG {org['name']} ID: {org['id']}")
            # Quando il nome della org è uguale a quella impostata
            if org['name'] == env_user.MERAKI_ORG:
                # Ottieni tutte le reti in questa org
                try:
                    response = _req(f"organizations/{org['id']}/networks", verify=True)

                    # Deserializziamo la risposta in un dizionario Python 
                    # in modo da poterci lavorare
                    networks = json.loads(response.text)

                    # Scorri la lista delle reti
                    for network in networks:
                        # print(f"Network: {network['name']}")
                        # print(network_wh)

                        # Quando il nome della rete è uguale a quella impostata
                        if network["name"] == network_wh:
                            # Prendi l'ID e memorizzalo nella variabile network_id
                            network_id = network["id"]
                            print(f"The Network ID for network {network_wh} is {network_id}")
                            # Ritorna il valore network_id
                            return network_id
                except Exception as e:
                    pprint(e)
    # Se la rete non è stata trovare restituisci il messaggio            
    return "No Network Found with that name"

# Imposta il webhook receiver in Meraki
def set_webhook_receiver(network_id, url, secret, server_name):
    print(f"Setting up webhook in the Meraki Network with id {network_id}...")

    try:
        # Creiamo il body come specificato nella documentazione per creare un webhook
        data = {
                "name": server_name,
                "url": url,
                "sharedSecret": secret
            }
        
        # Creiamo la richiesta per creare un nuovo webhook 
        # con i parametri passati come argomento
        response = _req(f"networks/{network_id}/webhooks/httpServers", method="post", jsonbody=data, verify=True)
        
        # Se la risposta è 201, allora la risorsa è stata creata
        if response.status_code == 201:
            print("Everything OK! Webhook configured in the Meraki Network")
            # Deserializziamo la risposta in un dizionario Python 
            # in modo da poterci lavorare
            https_server_id = json.loads(response.text)

            # Ritorna l'ID del webhook appena creato
            return https_server_id['id']
        else:
            # Altrimenti stampa un messaggio di errore
            print("Something went wrong")
            print(f"{response.status_code} - {response.text}")

    # Se ci sono delle eccezioni stampa il messaggio di errore
    # e restituisci il messaggio
    except Exception as e:
        pprint(e)
        return "Setting https server fail"


# Importa gli Alert in Meraki (imposta solo su 'settingsChanged')
def set_alerts(network_id, http_server_id):
    try:
        # Creiamo il body come specificato nella documentazione per impostare l'Alert
        data = {
                "defaultDestinations": {
                    "emails": [],
                    "snmp": False,
                    "allAdmins": False,
                    "httpServerIds": [http_server_id]
                },
                "alerts": [
                            {
                                "type": "settingsChanged",
                                "enabled": True,
                                "alertDestinations": {
                                    "emails": [],
                                    "snmp": False,
                                    "allAdmins": False,
                                    "httpServerIds": []
                                },
                                "filters": {}
                            }
                    ]
                }

        # Creiamo la richiesta per impostare l'alert 
        # con i parametri passati come argomento
        response = _req("networks/"+network_id+"/alerts/settings", method="put", jsonbody=data, verify=True)
        # Se lo status code della risposta è 200
        if response.status_code == 200:
            print("Everything OK! Webhook set in the Meraki Alerts Settings")
            # Ritorna lo status code
            return response.status_code

    # Se ci sono delle eccezioni stampa il messaggio di errore
    # e restituisci il messaggio
    except Exception as e:
        pprint(e)
        return "Alert Settings Failed"

# L'applicazione parte qui
if __name__ == "__main__":

    # Definiamo la variabile server_url come combinazione 
    # dell'URL + la porta nella forma URL:PORTA 
    server_url = env_user.WEBHOOK_URL+":"+env_user.WEBHOOK_PORT

    # Le richieste devono viaggiare in HTTPS quindi
    # se l'URL contiene http:// stampa il messaggio ed esci
    if "http://" in server_url:
        print("Make sure the Server URL starts with HTTPS.")
        exit(1)
    # Se nell'url c'è ngrok.io allora non impostare la porta
    # poichè l'URL esegue già il forwarding sulla porta corretta
    if "ngrok.io" in server_url:
        server_url = env_user.WEBHOOK_URL

    # Richiama tutte le funzioni create per ottenere i parametri di configurazione
    # Cerca il network ID della rete che abbiamo specificato nelle variabili d'ambiente
    network_id = get_network_id(env_user.MERAKI_NETWORK)
    # Elimina tutti i webhook presenti
    clear_webhooks(network_id)
    # Copia i valori delle variabili d'ambiente in variabili python
    secret = env_user.WEBHOOK_SECRET
    server_name = env_user.WEBHOOK_SERVER_NAME
    server_id = set_webhook_receiver(network_id, server_url, secret, server_name)
    # Se il valore restituito della funzione set_alerts() è 200 allora avvia l'applicazione
    if set_alerts(network_id, server_id) == 200: 
        app.run(host="0.0.0.0", port=env_user.WEBHOOK_PORT, debug=False)
    # Altrimenti c'è un errore
    else:
        print("Something went wrong...")
