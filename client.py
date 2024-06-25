import socket
import time
import threading

def get_remote_info():
    HOST = input("Enter remote peer's IP address: ")
    PORT = int(input("Enter remote peer's port: "))
    return HOST, PORT

def retry(t):
    max_dots = 3
    delay_between_dots = 0.5

    while not t.is_set():
        for i in range(1, max_dots + 1):
            print("Retrying" + "." * i, end="\r")
            time.sleep(delay_between_dots)
            print("Retrying" + " " * i, end="\r")  # Cancella i punti di sospensione

        # Resetta i punti di sospensione e ricomincia
        print("Retrying", end="\r")
        time.sleep(delay_between_dots)

def connection(HOST, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_established = threading.Event()

    max_attempts = 10
    delay_between_attempts = 3
    for attempt in range(max_attempts):
        try:
            client_socket.connect((HOST, PORT))
            connection_established.set()
            break
        except ConnectionRefusedError:
            print(f"Connection attempt {attempt+1}/{max_attempts} failed.\n")
            retry(connection_established)
            time.sleep(delay_between_attempts)
    
    if connection_established.is_set():
        print(f"Connected to peer on {HOST}:{PORT}")
        while True:
            message = input("")
            if message:
                client_socket.sendall(bytes(message, "utf-8"))
            else:
                break
        
            data = client_socket.recv(1024)
            if data:
                print(f"Received: {data.decode('utf-8')}")
            else:
                print("Peer disconnected.")
                break
    else:
        print("Connection failed after all attempts.")

    client_socket.close()

def main():
    HOST, PORT = get_remote_info()
    connection_thread = threading.Thread(target=connection, args=(HOST, PORT))
    connection_thread.start()

main()
