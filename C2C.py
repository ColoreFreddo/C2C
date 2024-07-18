import socket
import threading
import random
from nacl.public import PrivateKey, PublicKey, Box

# Fixed handshake port
handshake_port = 5000
handshake_ip = '0.0.0.0'  # Listen on all available interfaces

# Generate key pairs
private_key = PrivateKey.generate()
public_key = private_key.public_key

# Control variable to terminate the connection
terminate = threading.Event()

# Global variable to store the box for encryption/decryption
box = None

# Function to handle key exchange
def exchange_keys(sock, recv_first, send_ip, send_port):
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

# Function to handle port exchange
def exchange_ports(sock, recv_first, peer_ip):
    if recv_first:
        # Receive peer's dynamic port
        peer_port, _ = sock.recvfrom(1024)
        peer_port = int(peer_port.decode())
        # Send own dynamic port
        dynamic_port = random.randint(1025, 65535)
        sock.sendto(str(dynamic_port).encode(), (peer_ip, handshake_port))
    else:
        # Send own dynamic port first
        dynamic_port = random.randint(1025, 65535)
        sock.sendto(str(dynamic_port).encode(), (peer_ip, handshake_port))
        # Receive peer's dynamic port
        peer_port, _ = sock.recvfrom(1024)
        peer_port = int(peer_port.decode())

    return dynamic_port, peer_port

# Function to handle connection request
def handle_connection_request(sock, peer_ip):
    try:
        # Send connection request
        sock.sendto(b"Popi", (peer_ip, handshake_port))
        sock.settimeout(5)  # Set a timeout for the response

        # Wait for response
        response, _ = sock.recvfrom(1024)
        if response == b"Popipopi":
            print("Connection accepted by peer.")
            return True
        elif response == b"Nac":
            print("Connection refused by peer.")
            return False
        else:
            print("Unexpected response.")
            return False
    except socket.timeout:
        print("OOC: Client does not exist or did not respond.")
        return False

# Function to receive connection request
def receive_connection_request(sock):
    while not terminate.is_set():
        try:
            # Wait for connection request
            message, addr = sock.recvfrom(1024)
            if message == b"Popi":
                print(f"Connection request received from {addr[0]}")
                response = input("Do you want to accept the connection? (yes/no): ")
                if response.lower() == "yes":
                    sock.sendto(b"Popipopi", addr)
                    return addr[0]
                else:
                    sock.sendto(b"Nac", addr)
            else:
                print("Unexpected message received.")
        except Exception as e:
            print(f"Error receiving connection request: {e}")
            break

# Function to receive messages
def receive_message(peer_ip):
    # Handshake socket
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.bind((handshake_ip, handshake_port))

    # Perform port exchange
    dynamic_port, peer_port = exchange_ports(recv_socket, recv_first=True, peer_ip=peer_ip)
    recv_socket.close()

    # Create new socket with dynamic port
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.bind((handshake_ip, dynamic_port))

    # Perform key exchange
    exchange_keys(recv_socket, recv_first=True, send_ip=peer_ip, send_port=peer_port)
    
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
def send_message(user_name, peer_ip):
    # Handshake socket
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Perform connection request
    if not handle_connection_request(send_socket, peer_ip):
        return

    # Perform port exchange
    dynamic_port, peer_port = exchange_ports(send_socket, recv_first=False, peer_ip=peer_ip)

    # Create new socket with dynamic port
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_socket.bind((handshake_ip, dynamic_port))

    # Perform key exchange
    exchange_keys(send_socket, recv_first=False, send_ip=peer_ip, send_port=peer_port)
    
    while not terminate.is_set():
        try:
            message = input(f"{user_name}: ")
            encrypted_message = box.encrypt(message.encode())
            send_socket.sendto(encrypted_message, (peer_ip, peer_port))
            if message == "/bye":
                print("Connection terminated.")
                terminate.set()
                break
        except Exception as e:
            print(f"Error sending message: {e}")
            break

# Get user input for configuration
user_name = input("Enter your chat name: ")
mode = input("Do you want to initiate a connection or wait for a request? (initiate/wait): ")

if mode.lower() == "initiate":
    peer_ip = input("Enter the peer's IP address: ")
    # Create threads for sending and receiving
    recv_thread = threading.Thread(target=receive_message, args=(peer_ip,))
    send_thread = threading.Thread(target=send_message, args=(user_name, peer_ip))

    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()
else:
    # Wait for a connection request
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.bind((handshake_ip, handshake_port))

    peer_ip = receive_connection_request(recv_socket)
    if peer_ip:
        # Create threads for sending and receiving
        recv_thread = threading.Thread(target=receive_message, args=(peer_ip,))
        send_thread = threading.Thread(target=send_message, args=(user_name, peer_ip))

        recv_thread.start()
        send_thread.start()

        recv_thread.join()
        send_thread.join()

# Destroy keys
del private_key
del public_key
del box
