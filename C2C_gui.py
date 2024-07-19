import socket
import threading
import random
from nacl.public import PrivateKey, PublicKey, Box
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

# Fixed handshake port
handshake_port = 6969
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
                response = messagebox.askyesno("Connection Request", f"Accept connection from {addr[0]}?")
                if response:
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
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, f"Peer: {message}\n")
            chat_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to send messages
def send_message():
    global box
    message = message_entry.get()
    if message:
        try:
            encrypted_message = box.encrypt(message.encode())
            send_socket.sendto(encrypted_message, (peer_ip, peer_port))
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, f"You: {message}\n")
            chat_text.config(state=tk.DISABLED)
            message_entry.delete(0, tk.END)
            if message == "/bye":
                print("Connection terminated.")
                terminate.set()
                send_socket.close()
        except Exception as e:
            print(f"Error sending message: {e}")

# GUI Setup
root = tk.Tk()
root.title("Encrypted Chat")

chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=10)

chat_text = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED)
chat_text.pack(padx=10, pady=10)

message_entry = tk.Entry(chat_frame, width=50)
message_entry.pack(side=tk.LEFT, padx=10, pady=10)

send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=10, pady=10)

def start_connection():
    global peer_ip, peer_port, send_socket
    user_name = simpledialog.askstring("Input", "Enter your chat name:")
    mode = simpledialog.askstring("Input", "Do you want to initiate a connection or wait for a request? (initiate/wait):")

    if mode.lower() == "initiate":
        peer_ip = simpledialog.askstring("Input", "Enter the peer's IP address:")
        # Create threads for sending and receiving
        recv_thread = threading.Thread(target=receive_message, args=(peer_ip,))
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_socket.bind((handshake_ip, 0))
        if handle_connection_request(send_socket, peer_ip):
            dynamic_port, peer_port = exchange_ports(send_socket, recv_first=False, peer_ip=peer_ip)
            send_socket.close()
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_socket.bind((handshake_ip, dynamic_port))
            exchange_keys(send_socket, recv_first=False, send_ip=peer_ip, send_port=peer_port)
            recv_thread.start()
    else:
        # Wait for a connection request
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_socket.bind((handshake_ip, handshake_port))

        peer_ip = receive_connection_request(recv_socket)
        if peer_ip:
            # Create threads for sending and receiving
            recv_thread = threading.Thread(target=receive_message, args=(peer_ip,))
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dynamic_port, peer_port = exchange_ports(send_socket, recv_first=False, peer_ip=peer_ip)
            send_socket.close()
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_socket.bind((handshake_ip, dynamic_port))
            exchange_keys(send_socket, recv_first=False, send_ip=peer_ip, send_port=peer_port)
            recv_thread.start()

start_button = tk.Button(root, text="Start", command=start_connection)
start_button.pack(padx=10, pady=10)

root.mainloop()

# Destroy keys
del private_key
del public_key
del box
