"""import socket

# Indirizzo IP di destinazione
indirizzo_ip = "192.168.19.32"

# Crea un socket TCP
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connessione al server
try:
    socket_client.connect((indirizzo_ip, 6969))
    print(f"Connesso a {indirizzo_ip} sulla porta 6969")

    # Invio di un pacchetto di prova
    pacchetto_invio = bytes(f"Prova", "utf-8")
    socket_client.sendall(pacchetto_invio)
    print(f"Pacchetto inviato: {pacchetto_invio}")

    # Ricezione di un pacchetto di risposta
    pacchetto_ricezione = socket_client.recv(1024)
    print(f"Pacchetto ricevuto: {pacchetto_ricezione}")

except Exception as e:
    print(f"Errore: {e}")

# Chiusura della connessione
socket_client.close()
print("Connessione chiusa")"""

def __main__():
    port = 6969
    message = "Hello Clown!"

    c2c = C2C()
    local_ip, gateway, network,broadcast = c2c.get_local_ip_and_network()
    # reachable_endpoints = c2c.clowns_scan(port)
    c2c.send_message("POPI",broadcast)
