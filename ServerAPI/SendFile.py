import socket
import json

def choose_client(filename, available_file_list, clientDict, index_list):
     avail_client = available_file_list[filename]
     chosen_index = index_list[filename] % len(avail_client)
     # Update the index dict
     index_list[filename] = (chosen_index + 1) % len(avail_client)

     chosen_client = avail_client[chosen_index]

     return {'address': chosen_client[0], 'port': clientDict[chosen_client][1]}

def handle_fetch(client_socket, available_file_list, clientDict, index_list):
     # Extract client address
     client_address = client_socket.getpeername()

     # Send list of available file to client 
     list_of_file = available_file_list.keys()
     msg = "list " + ' '.join(map(str, list_of_file))
     client_socket.sendall(msg.encode('utf-8'))
     # print(f"Send list of available files to {client_address}")

     # Receive the chosen file and send the suitable client
     filename = client_socket.recv(1024).decode('utf-8')
     # print(filename)
     if len(filename) == 0:
          print("Connection closed by the client.")
          return
     # choosing the client for sending file
     chosen_client = choose_client(filename, available_file_list, clientDict,index_list)
     json_str = json.dumps(chosen_client, ensure_ascii=True)

     msg = "client " + json_str
     client_socket.sendall(msg.encode('utf-8'))
     # print(f"Send information of client {chosen_client} for {filename} to {client_address}")
