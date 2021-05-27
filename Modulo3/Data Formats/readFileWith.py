print("Scorrere e leggere ogni riga utilizzando with per aprire il file")

x = 1

# È possibile aprire il file utilizzando 'with'.
# 'with' fornisce una migliore gestione delle eccezioni e chiude il file

with open("my-file.txt") as file:
    for line in file:
        print("Line" + str(x) + ": " + line)
        x += 1
