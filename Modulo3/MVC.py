# Il dispositivo è il "Model" per un oggetto Device 
class Device:
    # Definiamo le proprietà di un dispositivo
    ipAddress = ""
    port = ""

    # Questo esempio è dimostrativo ma in uno scenario reale questi dati verrebbe da una sorgente esterna (API, files, etc..)
    @staticmethod
    def findDevice():
        # Definiamo una lista di dispositivi
        devices = []

        # Creiamo un oggetto di tipo "Device"
        d = Device()

        # Inizializziamo le variabili
        d.ipAddress = "192.168.1.1"
        d.port = "80"
        
        # Aggiungiamo il dispositivo alla lista dei dispositivi
        devices.append(d)

        # Creiamo un secondo device
        d = Device()
        d.ipAddress = "192.168.2.1"
        d.port = "443"

        # Aggiungiamo il dispositivo alla lista dei dispositivi
        devices.append(d)

        # Creiamo un secondo device
        d = Device()
        d.ipAddress = "192.168.3.1"
        d.port = "8080"

        # Aggiungiamo il dispositivo alla lista dei dispositivi
        devices.append(d)

        return devices


# Questa classe è il "View" per l'oggetto Device ed è responsabile di visualizzare l'output
class DeviceView:
    # Questo è l'unico metodo in questa classe per mostrare i dati, la class non è a conoscenza del numero di elementi o altre info
    # E' solo responsabile di mostrare i dati
    def showDevices(self, devices):
        for d in devices:
            print("-----------")
            print("IP Address:" + d.ipAddress)
            print("Port: " + d.port)
            print("-----------")


# Questa classe è il "Controller" per i dispositivi ed è responsabile di manipolare i dati in input
class DeviceController:
    def __init__(self):
        # Inizializziamo il tutto
        # Creiamo una lista di dispositivi. Restituiti dalla funzione findDevice()
        devices = Device.findDevice()

        # Chiamiamo il metodo DeviceView() per creare una vista e la funzione showDevices per mostrare i risultati
        v = DeviceView()
        v.showDevices(devices)

    # Il codice seguente è un opzione per filtrare i dispositivi in base ad un filtro, in questo caso c'è bisogno di una funzione filter() 
    # def filterDevices(self, filter):
    #    devices = Device.findDevice(filter)


# Chiama la classe principale (main) DeviceController per avviare l'app
c = DeviceController()
