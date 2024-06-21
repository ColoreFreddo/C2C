import socket

def get_remote_info():
  HOST = input("Enter remote peer's IP address: ")
  PORT = int(input("Enter remote peer's port: "))
  HOST, PORT = get_remote_info()
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((HOST, PORT))

  print(f"Connected to peer on {HOST}:{PORT}")

  while True:
    message = input("")
    if message:
      client_socket.sendall(message.encode('utf-8'))
    else:
      break
    
    data = client_socket.recv(1024).decode('utf-8')
    if data:
      print(f"Received: {data}")
    else:
      print("Peer disconnected.")
      break

  client_socket.close()

get_remote_info()