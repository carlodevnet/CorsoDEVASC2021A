
class Observer():
    # Questa è la funzione che verrà chiamata quando ci sarà un update
    def update(self, subject):
        print("Observer : Subject just updated and told me about it --> Notify")
        print("Observer : It's state is now " + str(subject._state))

# La maggior parte del lavoro avviene nella classe "Subject"


class Subject():
    # Definiamo uno stato iniziale - L'underscore significa che questa variable è privata e utilizzabile solo all'interno della classe
    _state = 0

    # Definiamo un array di observers - L'underscore significa che questa variable è privata e utilizzabile solo all'interno della classe
    _observers = []

    # Agganciamo un nuovo Observer al Subject per ricevere updates
    def attach(self, Observer):
        print("Observer: Attached to the Subject")
        self._observers.append(Observer)

    # Sganciamo l'Observer dal Subject per smettere di ricevere updates
    def detach(self, Observer):
        print("Observer: Detached from the Subject")
        self._observers.remove(Observer)

    # Funzione utilizzata per notificare tutti gli observers
    def notify(self):
        print("Subject: I'm notifying my observers.. :")
        # La notifica è inviata a tutti gli observer nell'array _observers
        for observers in self._observers:
            observers.update(self)

    # Funzione utilizzata per inviare gli aggiornamenti
    def updateState(self, n):
        print("Subject: I've received a state update!")
        self._state = n
        # Chiamando questa funzione verrà inviata una notifica all'Observers
        self.notify()

# Creiamo un Subject
s = Subject()

# Creiamo 3 Obserers
ob1 = Observer()
ob2 = Observer()
ob3 = Observer()

# Agganciamo gli observers al Soggetto
s.attach(ob1)
s.attach(ob2)
s.attach(ob3)

# Aggiorniamo lo stato come test
s.updateState(5)

# Sgaciamo l'observers dal Subject
s.detach(ob1)
s.detach(ob2)
s.detach(ob3)
