import json
import socket

def discover(server_socket, published_file):
    msg = json.dumps(published_file)
    server_socket.sendall(msg.encode('utf-8'))