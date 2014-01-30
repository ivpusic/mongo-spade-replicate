import socket
from network import ip


HOST_IP = ip.get_lan_ip()
HOST_NAME = socket.gethostname()
