# Corso DevNet Associate v1.0 - DEVASC2021/A  
#### Instructor: Stefano Pilla (spilla [at] netschool.it)  

##### Istruzione per l'utilizzo dello script per i webhook

## Requirements
- Python 3
- ngork (Scaricabile da: https://ngrok.com)
- Accesso ad una dashboard Meraki (è possibile creare un account gratuito e avere accesso in scrittura ad una dashboard per un tempo limitato oppure è possibile utilizzare la sandbox sul sito developer.cisco.com)
- Un account Webex Teams (per creare una room e generare la chiave API da utilizzare nello script)

## Procedura
- Creare una room Webex Teams dove far recapitare le notifiche (trovare l'id della room creata attraverso postman/python o direttamente dalla documentazione API)
- Installare le librerie presenti nel file **requirements.txt** con il comando: 
    `pip install -r requirements.txt`
(è consigliato creare un ambiente virtuale venv)
- Se necessario installare **ngrok** seguendo le istruzioni trovare sul sito, aprire un terminale e digitare il seguente comando
`ngrok http 5000`
questo comando creerà un link pubblico temporaneo che potrà essere utilizzato come URL del webhook (utilizzare il link con https)
- Aprire il file **env_user.py** e compilare le seguenti variabili:
--``WT_ACCESS_TOKEN='<il_tuo_access_token_webex>' # Da generare dal portale Webex``
--``WT_ROOM_ID='<id_della_room_dove_inviare_il_messaggio>' # Da ricavare attraverso postman/python o dalla documentazione API``
--``MERAKI_API_KEY='<la_tua_chiave_api_meraki>' # Da generare sulla dashboard Meraki (cliccare sul nome utente in alto a sinistra > my profile > API access > Generate new API Key``
--``MERAKI_NETWORK='<il_nome_la_rete_meraki_da_monitorare>' ``
--``MERAKI_ORG='<il_nome_della_org_meraki_in_cui_è_presente_la_rete>' ``
--`` WEBHOOK_SECRET='<la_shared_key_da_utilizzare>' # Impostare un password complessa``
--`` WEBHOOK_URL='<link_pubblico_del_webhook>' # Sostituire con l'indirizzo pubblico generato da ngrok (https)``
--`` WEBHOOK_PORT='5000' # Se necessario sostituire con la porta su cui il web server sarà il ascolto (default 5000)``
--`` WEBHOOK_SERVER_NAME='DevNet-Webhook' # L'etichetta da impostare nella dashboard meraki per questo webhook``

- Lanciare il bash script con il comando:
    `. ./env_user.py`
questo imposterà le variabili d'ambiente necessarie allo script. Verificare le variabili con il comando:
`env`
- Lanciare lo script con il comando **python3 meraki_sample_webhook_receiver.py** oppure attraverso Visual Code
- Attendere l'output che comunica che il server è in ascolto sull'IP del vostro pc sulla porta specificata
## Test dello script
### Test #1
- Aprire Postman e creare una nuova richiesta con i seguenti parametri:
-- **Method:** GET
-- **URL:** <l'url di ngrok generato dall'applicazione>
-- Inviare la richiesta
-- L'output atteso è il messaggio **GET ricevuta! L'endpoint API funziona correttamente!**

### Test #2
- Aprire Postman e creare una nuova richiesta con i seguenti parametri:
-- **Method:** GET
-- **URL:** <l'url di ngrok generato dall'applicazione>/test
-- Inviare la richiesta
-- L'output atteso è il messaggio **URL /test correttamente implementato e funzionante**

### Test #3
- Aprire la dashboard Meraki e andare nel menu **Network-Wide > Alerts** e verificare in fondo alla pagina che il webhook sia stato correttamente creato:
-- Cliccare sul pulsante **"Send test Webhook"**
-- Un messaggio di test dovrebbe essere stato recapitato nel canale webex 
-- Il log dello script Python, nel terminale riporta il messaggio intero in formato json.