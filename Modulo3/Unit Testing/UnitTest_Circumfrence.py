# Importiamo il modulo math per avere accesso alle librerie necessarie
import math
# Importiamo la libreria unittest per eseguire i test
import unittest

# This is the UNIT in the Unit Test
# cioè la porzione di codice che stiamo testando
# La formula per calcolare la circoferenze è raggio * 2 * 3,14 (pi-greco)
def calcCircumfrence(r):
    return r*2*math.pi

'''
Se stampiamo direttamente la funzione otteniamo un risultato,
ma come facciamo a sapere se il risultato è quello corretto?
'''
print(f"Il risultato della funzione passando 5 come raggio e': {calcCircumfrence(5)}")


# Creaiamo un metodo per testare il tutto in modo automatico
class TestMyCode(unittest.TestCase):

    # Creiamo un metodo che inizia test_ per identificare il Test Case
    def test_circumfrence(self):
        circum = calcCircumfrence(5)
        # Utilizziamo assertEqual per controllare che 2 valori sono uguali
        # In questo caso testiamo che l'output ottenuto sia effettivamente 
        # quello del nostro output con un input = 5
        self.assertEqual(circum, 31.41592653589793)

    def test_circumfrenceZero(self):
        circum = calcCircumfrence(0)
        # Utilizziamo assertEqual per controllare che la funzione ritorni 0
        # Questo casi in genere vengono chiamati "Edge Cases"
        # In questo caso la circonferenza di un cerchio di raggio 0 è uguale a 0
        self.assertEqual(circum, 0)

    # Testiamo che la funzione ritorni un errore se gli viene passata una stringa
    # Questo è un altro Edge Case
    #def test_circumfrenceInvalid(self):
    #    self.assertRaises(calcCircumfrence("DevNet"))

    # Questa funzione anche se definita non verrà eseguita poichè il nome non inizia per test
    def myfunc(self):
        return("DevNet")

# Questo è il metodo utilizzato per avviare i test
unittest.main()
