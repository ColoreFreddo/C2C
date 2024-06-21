import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 9696        # The port used by the server

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(f"Connected to server on port {PORT}")

    while True:
        message = input("")
        if message:
            client_socket.sendall(message.encode('utf-8'))
        else:
            break

    client_socket.close()

if __name__ == "__main__":
    main()