#!/bin/bash
export WT_ACCESS_TOKEN='<il_tuo_access_token_webex>' # Da generare dal portale Webex
export WT_ROOM_ID='<id_della_room_dove_inviare_il_messaggio>' # Da ricavare dal portale Webex

# Meraki API Key used in the Meraki Simulator
export MERAKI_API_KEY='<la_tua_chiave_api_meraki>' # Da generare sulla dashboard Meraki
export MERAKI_NETWORK='<la_rete_meraki_da_monitorare>' 
export MERAKI_ORG='<la_org_meraki_da_monitorare>'

# Webhook parameters to set into Meraki
export WEBHOOK_SECRET='<la_shared_key_da_utilizzare>' # Impostare un password complessa
export WEBHOOK_URL='<link_pubblico_del_webhook>' # Sostituire con l'indirizzo pubblico
export WEBHOOK_PORT='5000' # Sostituire con la porta su cui il web server sarà il ascolto
export WEBHOOK_SERVER_NAME='DevNet-Webhook' # L'etichetta da impostare in meraki per questo webhook