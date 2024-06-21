import socket
import netifaces
import ipaddress

class C2C:
    def __init__(self, endpoints=None):
        self.endpoints = endpoints if endpoints else []

    def send_message(self, message, dest_endpoint):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((dest_endpoint.ip, dest_endpoint.port))
                s.sendall(message.encode())
                response = s.recv(1024)
                return response.decode()
        except Exception as e:
            print(f"NAC from {dest_endpoint.name}: {e}")
            return None

    def popi(self, endpoint):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((endpoint.ip, endpoint.port))
                print(f"POPI POPI {endpoint.name}")
                return True
        except socket.error:
            print(f"NAC from {endpoint.name}")
            return False

    def get_local_ip_and_network(self):
        # Retrieve the default gateway and the interface associated with it
        gateway_info = netifaces.gateways().get('default', {}).get(netifaces.AF_INET)
        if not gateway_info:
            raise RuntimeError("Default gateway not found")

        gateway, interface = gateway_info

        # Retrieve the IP address and subnet mask associated with the interface
        iface_addresses = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if not iface_addresses:
            raise RuntimeError(f"No IPv4 address found on interface: {interface}")

        local_ip_info = iface_addresses[0]
        local_ip = local_ip_info['addr']
        netmask = local_ip_info['netmask']

        # Create an IP network object
        network = ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
        broadcast = network.broadcast_address
        return local_ip, gateway, network, broadcast

    def clowns_scan(self, port):
        
        reachable_endpoints = []
        for ip in network.hosts():
                endpoint = Endpoint(str(ip), port, f'{ip}:{port}')
                if self.popi(endpoint):
                    reachable_endpoints.append(endpoint)
        
        return reachable_endpoints

    def send_to_clowns(self, message, endpoints):
        for endpoint in endpoints:
            response = self.send_message(message, endpoint)
            print(f"Response from {endpoint.name}: {response}")

class Endpoint:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name