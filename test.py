import socket
import threading

class Client:
    def __init__(self, host, send_port, receive_port):
        self.host = host
        self.send_port = send_port
        self.receive_port = receive_port
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            # Connect to Client 2's receive port for sending messages
            self.send_socket.connect((self.host, self.receive_port))
            print(f"Connected to {self.host} on send port {self.receive_port}")

            # Connect to Client 2's send port for receiving messages
            self.receive_socket.connect((self.host, self.send_port))
            print(f"Connected to {self.host} on receive port {self.send_port}")

            # Start thread to receive messages
            threading.Thread(target=self.receive_messages).start()

            # Main loop to send messages
            while True:
                message = input("Client 1 (Send): ")
                if message.lower() == 'exit':
                    break
                self.send_socket.sendall(message.encode())

        except ConnectionRefusedError:
            print(f"Connection to {self.host} refused.")
        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.send_socket.close()
            self.receive_socket.close()
            print("Connections closed.")

    def receive_messages(self):
        while True:
            try:
                data = self.receive_socket.recv(1024)
                if not data:
                    break
                print(f"Client 1 (Receive): {data.decode()}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

def main():
    host = "172.20.10.2"  # Replace with Client 2's IP address
    send_port = 6969
    receive_port = 9696
    
    client = Client(host, send_port, receive_port)
    client.start()

if __name__ == "__main__":
    main()
