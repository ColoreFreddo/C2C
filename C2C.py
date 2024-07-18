import socket
import threading
from nacl.public import PrivateKey, PublicKey, Box

# Configuration for both peers
recv_ip = '0.0.0.0'
recv_port = 5000  # Change to the appropriate receiving port
send_ip = 'peer_ip'  # Change to the peer's IP address
send_port = 5001  # Change to the appropriate sending port

# Generate key pairs
private_key = PrivateKey.generate()
public_key = private_key.public_key

# Control variable to terminate the connection
terminate = threading.Event()

# Global variable to store the box for encryption/decryption
box = None

# Function to handle key exchange
def exchange_keys(sock, recv_first):
    global box
    if recv_first:
        # Receive peer's public key first
        received_key, _ = sock.recvfrom(1024)
        peer_public_key = PublicKey(received_key)
        # Send own public key
        sock.sendto(bytes(public_key), (send_ip, send_port))
    else:
        # Send own public key first
        sock.sendto(bytes(public_key), (send_ip, send_port))
        # Receive peer's public key
        received_key, _ = sock.recvfrom(1024)
        peer_public_key = PublicKey(received_key)

    # Create the box for encryption/decryption
    box = Box(private_key, peer_public_key)
    print("Key exchange complete. Encrypted communication started.")

# Function to receive messages
def receive_message():
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.bind((recv_ip, recv_port))

    # Perform key exchange
    exchange_keys(recv_socket, recv_first=True)
    
    while not terminate.is_set():
        try:
            encrypted_message, _ = recv_socket.recvfrom(4096)
            message = box.decrypt(encrypted_message).decode()
            if message == "/bye":
                print("Connection terminated by the other user.")
                terminate.set()
                break
            print(f"Encrypted message received: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to send messages
def send_message():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Perform key exchange
    exchange_keys(send_socket, recv_first=False)
    
    while not terminate.is_set():
        message = input("You: ")
        encrypted_message = box.encrypt(message.encode())
        send_socket.sendto(encrypted_message, (send_ip, send_port))
        if message == "/bye":
            print("Connection terminated.")
            terminate.set()
            break

# Create threads for sending and receiving
recv_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()

# Destroy keys
del private_key
del public_key
del box
