# Importiamo la libreria unittest
import unittest

# Importiamo i moduli per l'utilizzo delle funzioni
import UnitTestCalc


class TestCalc(unittest.TestCase):
    # Scriviamo i metodi che iniziamo con test_

    # Testiamo l'addizione
    def test_add(self):
        self.assertEqual(UnitTestCalc.add(10, 5), 15)
        self.assertEqual(UnitTestCalc.add(-1, 1), 0)
        self.assertEqual(UnitTestCalc.add(-1, -1), -2)

    # Testiamo la sottrazione
    def test_subtract(self):
        self.assertEqual(UnitTestCalc.subtract(10, 5), 5)
        self.assertEqual(UnitTestCalc.subtract(-1, 1), -2)
        self.assertEqual(UnitTestCalc.subtract(-1, -1), 0)

    # Testiamo la moltiplicazione
    def test_multiple(self):
        self.assertEqual(UnitTestCalc.multiply(10, 5), 50)
        self.assertEqual(UnitTestCalc.multiply(-1, 1), -1)
        self.assertEqual(UnitTestCalc.multiply(-1, -1), 1)

    # Testiamo la divisione
    def test_divide(self):
        self.assertEqual(UnitTestCalc.divide(10, 5), 2)
        self.assertEqual(UnitTestCalc.divide(-1, 1), -1)
        self.assertEqual(UnitTestCalc.divide(-1, -1), 1)
        self.assertEqual(UnitTestCalc.divide(5, 2), 2.5)

        # Questo test ci permette di testare il l'eccezione per la divisione per 0
        with self.assertRaises(ValueError):
            UnitTestCalc.divide(10, 0)

# Verifichiamo che l'attributo __name__ sia __main__ e se vero richiama
# la funzione unittest.main() per avviare i test
if __name__ == "__main__":
    unittest.main()
