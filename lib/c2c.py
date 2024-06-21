import socket

class C2C:
    def __init__(self, endpoint1, endpoint2):
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2

    def send_request(self, message, dest_endpoint):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((dest_endpoint.ip, dest_endpoint.port))
                s.sendall(message.encode())
                response = s.recv(1024)
                return response.decode()
        except Exception as e:
            print(f"NAC from {dest_endpoint.name}: {e}")
            return None

    def check_host(self, endpoint):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(4)
                s.connect((endpoint.ip, endpoint.port))
                print("POPI POPI")
                return True
        except socket.error:
            print("NAC")
            return False

class Endpoint:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name