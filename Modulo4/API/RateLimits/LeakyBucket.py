# Author: Stefano Pilla 

# Descrizione: Questo codice è stato creato per la dimostrazione dell'algoritmo leaky-bucket
# utilizzato anche nel network traffic shaping e nel QoS (Quality of Service)
# Original Source Code: https://github.com/HirenAmbekar/Leaky-Bucket-Algorithm-Demonstration

import os

# Define a Server Class to simulate a client 
class Server:
    # Class Constructor 
    # Inizializza il rate e il bucket non appena l'oggetto viene creato
    def __init__(self, rate=int, data=[]):
        self.rate = rate
        self.data = data

    # Questo metodo viene chiamato quando i metodi print() o str() vengono utilizzate
    # con un oggetto di questa classe 
    def __str__(self):
        # Ritorna una stringa con il rate e i dati nel bucket
        return str([str(self.rate), str(self.data)])


# Definiamo una classe per il Buffer 
class Buffer:
    # Class Constructor 
    # Impostiamo il rate e il bucket quando viene creato l'oggetto 
    def __init__(self, buffer_size=int, buffer=[]):
        self.buffer_size = buffer_size
        self.buffer = buffer

    # Questo metodo aiuta a controllare lo stato del buffer
    # Se la lunghezza == 0 allora il buffer è vuoto
    def checkstate(self):
        if len(self.buffer) == 0:
            return True

    # Questo metodo viene chiamato quando i metodi print() o str() vengono utilizzate
    # con un oggetto di questa classe 
    def __str__(self):
        return str([str(self.buffer_size), str(self.buffer)])


# Impostiamo lo stato iniziale a True
basestate = True

# Definiamo il tempo da considerare (in questo caso 1 secondo)
# Questo definisce il "rate"
sec = 1

# Creiamo un oggetto buffer e impostiamo la sua capacità (ad esempio 80)
buffer = Buffer(int(input("Enter buffer size: ")))

# Creiamo un oggetto Server per simulare un API Endpoint (lato server)
# e settiamo il rate (ad esempio a 10)
server = Server(int(input("Enter server acceptance rate in bps: ")))

# Fintanto che lo stato è true 
while basestate:
    # Chiediamo all'utente di inserire una stringa da inviare al server
    data_to_send = input("Enter a string to be sent to the server: ")
    # Impostiamo il contatore a 0
    count = 0
    # Verifichiamo lo stato del buffer e se ==0 continua
    if buffer.checkstate():
        # Scorri la stringa
        for i in range(0, len(data_to_send)):
            # Se il server rate può accettare ancora dei dati
            if i < server.rate:
                # Aggiungi i dati al bucket
                server.data.append(data_to_send[i])
            # Se il server non può accettare dati (il rate è stato superato)
            else:
                # Verifica che il bufferr abbia abbastanza spazio
                if count < buffer.buffer_size:
                    # Aggiungi i dati al buffer
                    buffer.buffer.append(data_to_send[i])
                    count = len(buffer.buffer)
                # Altrimenti, se il buffer non ha più spazio
                else:
                    # Rifiuta i pacchetti
                    print("Data loss " + data_to_send[i])

    # Altrimenti, se il buffer non è uguale a 0 (cioè non è vuoto)
    else:
        j = 0
        # Crea un iteratore che scorre la dimensione totale dei dati da inviare
        # sommato alla lunghezza del buffer (non vuoto) 
        for i in range(0, len(data_to_send)+len(buffer.buffer)):
            # Se il contatore è < del rate 
            if i < server.rate:
                # se il buffer NON è vuoto, cioè len(buffer.buffer) ha una lunghezza (quindi = True) 
                if len(buffer.buffer):
                    # Aggiungi i dati in coda al bucket
                    server.data.append(buffer.buffer[0])
                    # e cancellali dal buffer
                    del buffer.buffer[0]
                # se il buffer è vuoto allora semplicemente aggiungi i dati
                # nel bucket
                else:
                    server.data.append(data_to_send[j])
                    j += 1
            # Altrimenti se il contatore NON è < del rate 
            else:
                # Controlla se il buffer ha ancora spazio
                if len(buffer.buffer) <= buffer.buffer_size:
                    # Controlla se la lunghezza del dato da inserire è maggiore dell'iteratore
                    if j < len(data_to_send):
                        # Aggiungi i dati nel buffer
                        buffer.buffer.append(data_to_send[j])
                        # Aumenta il contatore
                        j += 1
                # Altrimenti, se il buffer è pieno
                else:
                    # Altrimenti, se il buffer è pieno, scarta il pacchetto
                    if j < len(data_to_send):
                        print("Data loss " + data_to_send[j])
                        j += 1

    print("This is the data rate and the data accepted by the Server: ")
    print(server)
    
    print("This is the da in the buffer: ")
    print(buffer)
    print("*" * 30)
   