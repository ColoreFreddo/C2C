import socket
import threading

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 6969        # Port to listen on (non-privileged ports are > 1023)

client_list = []


def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                # Broadcast message to all clients
                for client in client_list:
                    if client != client_socket:
                        client.sendall(data.encode('utf-8'))
            else:
                # Client disconnected
                remove_client(client_socket)
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            remove_client(client_socket)
            break

def remove_client(client_socket):
    client_list.remove(client_socket)
    client_socket.close()
    print(f"Client disconnected: {client_socket.getpeername()}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on port {PORT}")

    while True:
        client_socket, address = server_socket.accept()
        client_list.append(client_socket)
        print(f"Connected by {address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()