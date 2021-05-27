# Definiamo una classe Employee con le proprietà richieste
class Employee:
    # Definiamo un valore di 1.05 come aumento sullo stipendio
    raise_amt = 1.05

    # Metodo Costruttore per definire i valori iniziali dell'oggetto creato
    # utilizzando i valori passati come argomento
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    # Definiamo un metodo email che ci restituisca la mail
    # nel formato nome.cognome@email.com
    def email(self):
        return f"{self.first}.{self.last}@email.com"

    # Definiamo un metodo fullname che ci restituisca il nome completo
    def fullname(self):
        return f"{self.first} {self.last}"

    # Definiamo un metodo apply_raise per l'aumento di stipendio
    # con il valore definito in precedenza
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)
