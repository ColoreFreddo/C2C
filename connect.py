import socket
import time

def get_remote_info():
  HOST = input("Enter remote peer's IP address: ")
  PORT = int(input("Enter remote peer's port: "))
  return HOST, PORT

def main():
  HOST, PORT = get_remote_info()
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connection_established = False

  max_attempts = 5
  delay_between_attempts = 5
  for attempt in range(max_attempts):
    try:
      client_socket.connect((HOST, PORT))
      connection_established = True
      break
    except ConnectionRefusedError:
      print(f"Connection attempt {attempt+1}/{max_attempts} failed. Retrying in {delay_between_attempts} seconds...")
      time.sleep(delay_between_attempts)
  
  if connection_established:
    print(f"Connected to peer on {HOST}:{PORT}")
    while True:
      message = input("")
      if message:
        client_socket.sendall(bytes(message, "utf-8"))
      else:
        break
    
      data = bytes(client_socket.recv(1024))
      if data:
        print(f"Received: {data}")
      else:
        print("Peer disconnected.")
        break
  else:
    print("Connection failed after all attempts.")

  client_socket.close()

main()