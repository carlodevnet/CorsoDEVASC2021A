# Definiamo delle funzioni per l'esecuzione delle operazioni

# Addizione
def add(x, y):
    return x+y

# Sottrazione
def subtract(x, y):
    return x-y

# Moltiplicazione
def multiply(x, y):
    return x*y

# Divisione
def divide(x, y):
    if (y == 0):
        raise ValueError("Can not divide by zero")
    return x / y

# Potremmo testare in questo modo tutte le funzioni ma questa soluzione non è scalabile quando ci sono molte funzioni da testare
# print(add(3, 5))
# print(subtract(5, 2))
# ....