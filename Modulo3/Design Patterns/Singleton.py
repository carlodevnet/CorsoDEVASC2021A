# Definizione della classe ConfigValues 
class ConfigValues:
    # Il doppio underscore significa che l'attributo verrà reso privato e riscritto da Python per evitare conflitti (name mangling)
    # L'interprete Python riscrive il nome della variabile in _classname__<nome_variabile> in modo da evitare collisioni quando si 
    # utilzza la classe in modo estensivo
    __instance = None

    # Un metodo Statico significa che la funzione può essere chiamata anche se l'istanza della classe non è stata creata 
    # In questo caso il metodo "getter" per ottenere lo stato della classe
    @staticmethod
    def getInstance():
        if ConfigValues.__instance == None:
            ConfigValues()
        return ConfigValues.__instance

    # Il costruttore __init__ permette di inizializzare la classe. E' il metodo che viene automaticamente chiamato quando si 
    # crea un oggetto di questa classe.
    def __init__(self):
        """ Virtually private constructor. """
        if ConfigValues.__instance != None:
            raise Exception("This Class is a singleton")
        else:
            ConfigValues.__instance = self


# Non creiamo un oggetto ConfigValue ma richiamamo il metodo getInstance() (è possibile farlo poichè getInstance è un metodo statico)
# Questo creerà la prima istanza della classe. Il valore di ConfigValues.__instance == None quindi l'istanza verrà creata
s = ConfigValues.getInstance()
print(s)

# La seconda volta verrà invece restituta l'istanza creata in precedenza perchè __instance != None
s = ConfigValues.getInstance()
print(s)

# Questa istruzione invece creerà una nuova istanza della classe. Questa volta però verrà sollevata un'eccezione poichè l'istanze è 
# stata già creata dalla prima chiamata getInstance()
s = ConfigValues()
print(s)
