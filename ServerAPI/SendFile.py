import socket
import json

def choose_client(filename, available_file_list, clientDict, index_list):

     try:
          avail_client = available_file_list[filename]
          chosen_index = index_list[filename] % len(avail_client)
          # Update the index dict
          index_list[filename] = (chosen_index + 1) % len(avail_client)

          chosen_client = avail_client[chosen_index]

          return {'address': chosen_client[0], 'port': clientDict[chosen_client][1]}

     except Exception as e:
          print("Error in choosing client:", e)
          return None

def handle_fetch_file(client_socket, available_file_list):
     r"""
          Return a list of available file names to the requesting client
     """

     # Send list of available file to client 
     list_of_file = [fname for fname in available_file_list.keys()]
     msg = json.dumps(list_of_file)
     client_socket.sendall(msg.encode('utf-8'))

def handle_fetch_owner(client_socket, filename, available_file_list, clientDict, index_list):
     r"""
          Return the owner information which holding the specific file name that send from the requesing client
     """

     if len(filename) == 0:
          return
     # choosing the client for sending file
     chosen_client = choose_client(filename, available_file_list, clientDict, index_list)
     json_str = json.dumps(chosen_client, ensure_ascii=True)

     print(f"Send owner {json_str} to client")
     client_socket.sendall(json_str.encode('utf-8'))