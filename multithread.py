import threading
import time

# Event per sincronizzare i due thread
connection_event = threading.Event()

# Funzione per visualizzare dinamicamente la scritta "Retrying"
def display_retrying():
    while not connection_event.is_set():
        for i in range(1, 4):
            print("Retrying" + "." * i, end="\r")
            time.sleep(0.5)
            print("Retrying" + " " * i, end="\r")
        print("Retrying", end="\r")
        time.sleep(0.5)

# Funzione per eseguire i tentativi di connessione in background
def background_connection():
    # Simulazione di tentativi di connessione
    for i in range(1, 6):
        print(f"Tentativo di connessione {i}")
        time.sleep(3) 
        if i == 3:
            connection_event.set()  # Simula una connessione riuscita al terzo tentativo
            break
       
    if connection_event.is_set():
        print("Connessione avvenuta con successo")
    if not connection_event.is_set():
        print("Connessione non riuscita dopo tutti i tentativi.")

# Avvia il thread per eseguire i tentativi di connessione in background
connection_thread = threading.Thread(target=background_connection)
connection_thread.start()

# Avvia il thread per visualizzare dinamicamente la scritta "Retrying"
retrying_thread = threading.Thread(target=display_retrying)
retrying_thread.start()

# Attendi che il thread di visualizzazione termini
retrying_thread.join()

# Attendi che il thread di connessione termini
connection_thread.join()
