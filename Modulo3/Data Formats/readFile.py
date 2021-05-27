
# Utilizzare il metodo open per aprire un file
# Passare il nome del file da aprire e mode. 'r' per la sola lettura 'w' se si desidera scrivere nel file

my_file_object = open("my-file.txt",  "r")
print("Leggi l'intero file:")

# read() le letture nell'intero file. In questa riga di codice si legge il contenuto del file e lo si stampa sullo schermo.
print(my_file_object.read())
print("\n")

# .close chiude il file

my_file_object.close()
