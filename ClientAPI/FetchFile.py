import socket
import json
import os

from . import ClientUI

def fetch(serverIP, serverPort, repoPath):
     # Extract server address
     try:
          server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          server_socket.connect((serverIP, serverPort))
     except Exception as e:
          print("Cannot connect to server")
          return

     msg = "fetch"
     server_socket.sendall(msg.encode('utf-8'))
     print(f"Send fetch requests to server")

     for _ in range(2):
          msg = server_socket.recv(1024).decode('utf-8')
          if len(msg) == 0:
               print("Connection closed by the server.")
               break
          print(f"Received message from server: {msg}")

          # Check the type of message from client. 
          msg = msg.split(None, 1)
          if msg[0] == "list": # return a list of available file from fetch request. User will choose a file, then client will send the request for info of that file
               chosen_file = ClientUI.display_available_file(msg[1])
               server_socket.sendall(f"{chosen_file}".encode('utf-8'))
          elif msg[0] == "client": # return the info of a client having the chosen file
               fetch_from_client(chosen_file, repoPath, msg[1])

     server_socket.close()


def fetch_from_client(chosen_file, repoPath, data):
     target_address = json.loads(data)
     # print(target_address)
     fetch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     fetch_socket.connect((target_address['address'], target_address['port']))

     msg = f"{chosen_file}"
     fetch_socket.sendall(msg.encode('utf-8'))
     with open(f'{os.path.join(repoPath, chosen_file)}', 'wb') as file:
          data = fetch_socket.recv(4096)  # Adjust buffer size as per your requirements
          file.write(data)
     print(f"Fetch {chosen_file} successfully")

     fetch_socket.close()

def discover(server_socket, published_file):
     msg = json.dumps(published_file)
     server_socket.sendall(msg.encode('utf-8'))
