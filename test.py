import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

        # Start a thread to receive messages from the server
        threading.Thread(target=self.receive_messages).start()

        # Main loop to send messages
        while True:
            message = input("Client 1: ")
            if message.lower() == 'exit':
                break
            self.client_socket.sendall(message.encode())

        self.client_socket.close()
        print("Connection closed.")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"Client 2: {data.decode()}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

def main():
    host = "192.168.19.32"  # Replace with Client 2's IP address
    port = 6969
    
    client = Client(host, port)
    client.start()

if __name__ == "__main__":
    main()
