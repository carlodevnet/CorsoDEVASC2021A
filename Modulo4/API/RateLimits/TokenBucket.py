# Author: Stefano Pilla 

# Descrizione: Questo codice è stato creato per la dimostrazione dell'algoritmo token-bucket
# Source code: https://dev.to/satrobit/rate-limiting-using-the-token-bucket-algorithm-3cjh

import time

class TokenBucket:

    # Costruttore per la classe TokenBucket
    def __init__(self, tokens, time_unit, forward_callback, drop_callback):
        # la variabile tokens, contiene il numero di gettoni 
        # aggiunti al bucket in ogni unità di tempo
        self.tokens = tokens

        # time_unit: i token vengono aggiunti in questo frame temporale
        self.time_unit = time_unit

        # forward_callback: questa funzione è chiamata quando il pacchetto viene inoltrato
        self.forward_callback = forward_callback

        # drop_callback: questa funzione è chiamata quando il pacchetto viene scartato
        self.drop_callback = drop_callback

        # Inserisci tutti i token nel bucket
        self.bucket = tokens

        # Questa variabile viene utilizzata per tenere traccia 
        # dell'ultima volta che il bucket è stato controllato
        # di default è impostato al tempo di quando è stato creato il bucket
        self.last_check = time.time()

    # Definiamo gli handler method per gestire i pacchetti in arrivo
    def handler(self, packet):
        # Controlliamo il tempo attuale
        current = time.time()

        # Impostiamo il tempo passato con la differenza del momento corrente 
        # meno il tempo dell'ultima volta che è stato controllato il bucket
        time_passed = current - self.last_check

        # Il valore last_check viene aggiornato
        self.last_check = current

        # Moltiplicando il tempo passato e il nostro rate (che è il risultato di tokens / time_unit)
        # possiamo capire quanti token devono essere aggiunti al bucket
        self.bucket = self.bucket + time_passed * (self.tokens / self.time_unit)

        # Resettiamo il bucket se ci sono più tokens del valore di default
        if (self.bucket > self.tokens):
            self.bucket = self.tokens

        # Se il bucket non ha abbastanza token, scarta il pacchetto
        if (self.bucket < 1):
            self.drop_callback(packet)

        # Altrimenti, rimuovi un token e inoltra il pacchetto
        else:
            self.bucket = self.bucket - 1
            self.forward_callback(packet)

# Questa funzione semplicemente scrive una stringa 
# per indicare che il pacchetto è stato inoltrato
def forward(packet):
    print("Packet Forwarded: " + str(packet))

# Questa funzione semplicemente scrive una stringa 
# per indicare che il pacchetto è stato scartato
def drop(packet):
    print("Packet Dropped: " + str(packet))

# Creiamo un bucket con 1 solo token
throttle = TokenBucket(5, 1, forward, drop)

packet = 0

# Avviamo il ciclo
while True:
    # Cambiare questi valori per testare l'algoritmo
    time.sleep(0.3)
    throttle.handler(packet)
    packet += 3