import socket
import json

def ping(clientInfo) -> bool:
   r'''
    clientInfo: a dictionary format {'Address', 'Name', 'serverHandlerPort', 'ClientHandlerPort'}

    return true if the client is alive, else return false
   '''
   try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
         client_socket.settimeout(5)  # Set a timeout for the connection attempt
         client_socket.connect((clientInfo['address'], clientInfo['serverHandlerPort']))
         client_socket.sendall("ping".encode())
         
         jsonStr = client_socket.recv(1024).decode()
         if jsonStr == "":
            return False
         else: 
            return True  # Connection successful and response received

   except (socket.error, socket.timeout) as e:
      print(f"Error connecting to {clientInfo['name']}: {e}")
      return False  # Connection error or timeout

   except Exception as e:
      print(f"Error in ping: {e}")
      return False  # Other unexpected errors

