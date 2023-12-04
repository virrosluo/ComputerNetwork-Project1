import socket
import json
import os

# def fetch(serverIP, serverPort, repoPath, clientInfo):
#     try:
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.connect((serverIP, serverPort))
#     except Exception as e:
#         print("Cannot connect to server")
#         return

#     msg = "fetch"
#     server_socket.sendall(msg.encode('utf-8'))
#     print(f"Send fetch requests to server")

#     for _ in range(2):
#         msg = server_socket.recv(1024).decode('utf-8')
#         if len(msg) == 0:
#             print("Connection closed by the server.")
#             break
#         print(f"Received message from server: {msg}")

#         # Check the type of message from client. 
#         msg = msg.split(None, 1)
#         if msg[0] == "list": # return a list of available file from fetch request. User will choose a file, then client will send the request for info of that file
#             chosen_file = clientInfo.UI.display_available_file(msg[1])
#             server_socket.sendall(f"{chosen_file}".encode('utf-8'))
#         elif msg[0] == "client": # return the info of a client having the chosen file
#             fetch_from_client(chosen_file, repoPath, msg[1])

#     server_socket.close()


def fetch_from_server(serverIP, serverPort):
    r"""
        Used to fetch all files that server is holding for user to choose

        return a list of files
    """

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((serverIP, serverPort))
        server_socket.sendall("fetch".encode())
        print(f"Send fetch file requests to server")

        msg = server_socket.recv(2048).decode()
        server_socket.close()

        print(f"Received files from server: {msg}")

        msg = list(json.loads(msg))
        print(msg)
        return msg
    except Exception as e:
        print("Cannot connect to server")

    
def fetch_file_owner(serverIP, serverPort, fileName):
    r"""
        Fetch Client that holding the specific "fileName" for the requesting client

        return: {'address': IPAddress, 'port': Int}
    """

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((serverIP, serverPort))
    except Exception as e:
        print("Cannot connect to server")

    msg = f"owner\n{fileName}"
    server_socket.sendall(msg.encode('utf-8'))
    print("Send fetch owner requests to server")

    msg = server_socket.recv(1024).decode('utf-8')
    server_socket.close()

    print(f"Received owners from server: {msg}")
    return dict(json.loads(msg))

def fetch_from_client(chosen_file, repoPath, target_address):
    r"""
        Send a request fetch file data to the "target_address" that holding the specific file

        target_address: {'address': IPAddress, 'port': Int}
    """
    try:
        fetch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fetch_socket.connect((target_address['address'], target_address['port']))

        msg = f"{chosen_file}"
        fetch_socket.sendall(msg.encode('utf-8'))
        with open(f'{os.path.join(repoPath, chosen_file)}', 'wb') as file:
            data = fetch_socket.recv(4096)
            while(data):
                file.write(data)
                data = fetch_socket.recv(4096)
        print(f"Fetch {chosen_file} successfully")
        fetch_socket.close()

        return True
    except Exception as e:
        print(f"Fetch {chosen_file} failed: {e}")
        return False