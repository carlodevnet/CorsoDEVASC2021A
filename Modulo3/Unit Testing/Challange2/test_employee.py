import unittest
from employee import Employee


class TestEmployee(unittest.TestCase):

    # Definiamo il metodo SetUpClass(cls) che verrà richiamato prima 
    # dell'esecuzione dei test
    @classmethod
    def setUpClass(cls):
        print('Setup Class')

    # Definiamo il metodo tearDownClass(cls) che verrà richiamato alla fine 
    # dell'esecuzione dei test
    @classmethod
    def tearDownClass(cls):
        print('\nTearDown Class')

    # Definiamo il metodo setUp(self) per inizializzare gli oggetti
    # da utilizzare durante l'esecuzione dei test
    def setUp(self):
        print("Setting up the objects...")
        self.emp_1 = Employee("John", "Doe", 50000)
        self.emp_2 = Employee("Sue", "Smith", 60000)

    # Definiamo il metodo tearDown(self) per distruggere gli oggetti
    # utilizzati durante l'esecuzione dei test
    def tearDown(self):
        print("tearDown\n")
        print("Destroying the objects...\n")
        pass

    # Definiamo il metodo test_email(self) per testare che il valore restituito
    # dalla funzione email sia effettivamente nome.cognome@email.com
    def test_email(self):
        print("test_email")
        self.assertEqual(self.emp_1.email, 'John.Doe@email.com')
        self.assertEqual(self.emp_2.email, 'Sue.Smith@email.com')

        # Proviamo a cambiare nome da John a Corey e da Sue a Jane
        # per avere una ulteriore conferma che l'email restituita è ancora nome.cognome@email.com
        self.emp_1.first = "Corey"
        self.emp_2.first = "Jane"

        self.assertEqual(self.emp_1.email, 'Corey.Doe@email.com')
        self.assertEqual(self.emp_2.email, 'Jane.Smith@email.com')

    # Definiamo il metodo test_fullname(self) per testare che il valore restituito
    # dalla funzione fullname sia effettivamente Nome Cognome
    def test_fullname(self):
        print("test_fullname")
        self.assertEqual(self.emp_1.fullname, 'John Doe')
        self.assertEqual(self.emp_2.fullname, 'Sue Smith')

        # Proviamo a cambiare nome da John a Corey e da Sue a Jane
        # per avere una ulteriore conferma che il nome completo restituito 
        # sia Nome Cognome
        self.emp_1.first = "Corey"
        self.emp_2.first = "Jane"

        self.assertEqual(self.emp_1.fullname, 'Corey Doe')
        self.assertEqual(self.emp_2.fullname, 'Jane Smith')

    # Definiamo il metodo test_apply_raise(self) per testare che il valore restituito
    # dalla funzione apply_raise sia il valore attuale * il valore definito nella 
    # variabile raise_amt
    def test_apply_raise(self):
        print("test_apply_raise")
        self.emp_1.apply_raise()
        self.emp_2.apply_raise()

        # L'oggetto emp_1 ha come paga base 50000 che moltiplicato * 1,05 dovrebbe essere
        # uguale a 52500
        # L'oggetto emp_2 ha come paga base 60000 che moltiplicato * 1,05 dovrebbe essere
        # uguale a 63000
        self.assertEqual(self.emp_1.pay, 52500)
        self.assertEqual(self.emp_2.pay, 63000)

# Verifichiamo che l'attributo __name__ sia __main__ e se vero richiama
# la funzione unittest.main() per avviare i test
if __name__ == "__main__":
    unittest.main()
