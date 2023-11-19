import os
import socket
import json
import threading

from ClientAPI.FetchFile import fetch
from ClientAPI.PublishFile import publish, discover
from ClientAPI.ClientUI import ClientUI
from ClientAPI.SendFile import handle_fetch_request

class Client:
    def __init__(self, 
                 serverInfo:tuple,
                 clientName:str,
                 serverHandlerInfo:tuple,
                 clientHandlerInfo:tuple,
                 SupplyingFile_number,
                 clientUI) -> None:
        self.serverIP, self.serverPort = serverInfo

        self.serverHandlerIP, self.serverHandlerPort = serverHandlerInfo
        self.clientHandlerIP, self.clientHandlerPort = clientHandlerInfo
        self.clientName = clientName
        self.supplyingFile_number = SupplyingFile_number

        self.UI = clientUI

        self.repoPath = 'repository'
        self.published_file = []
        if os.path.exists(self.repoPath):
            for fname in os.listdir(self.repoPath):
                # print(fname)
                self.published_file.append(fname)
        else: os.mkdir(self.repoPath)

    def handle_client(self, connectionSocket):
        # Create new thread to handle a new client fetch request
        while True:
            clientSocket, _ = connectionSocket.accept()
            task = threading.Thread(target=handle_fetch_request,
                                    args=(clientSocket, self.repoPath))
            task.start()

    def handle_server(self, connectionSocket):
        while True:
            serverSocket, _ = connectionSocket.accept()
            
            msg = serverSocket.recv(1024).decode('utf-8')
            msg = msg.split(' ')

            if msg[0] == "discover":
                discover(serverSocket, self.published_file)
            elif msg[0] == "ping":
                serverSocket.sendall("ping".encode())

    def handle_UI(self):
        while True:
            command = input("Input command: ")
            command = command.split(' ')

            if command[0] == 'display':
                self.UI.display_published_file(self.published_file)

            elif command[0] == 'fetch':
                fetch(self.serverIP, self.serverPort, self.repoPath, self)

            elif command[0] == 'publish':
                publish(command[1], self.repoPath, self.serverIP, self.serverPort, self)
                _, fname = os.path.split(command[1])
                if  fname not in self.published_file:
                    self.published_file.append(fname)

            elif command[0] == 'exit':
                print(f'Client {self.clientName} shut down')
                return
            else:
                print("Undefined command")

    def init_connection(self) -> bool:
        r'''
        Use to create the connection between the server and the client.
        Let the server know the information about the client at the start and then end.
        '''
        data = {
            'clientName': self.clientName,
            'serverHandlerPort': self.serverHandlerPort,
            'clientHandlerPort': self.clientHandlerPort,
            'repository': self.published_file
        }
        json_str = json.dumps(data, ensure_ascii=True)

        try:
            server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_connection.connect((self.serverIP, self.serverPort))
            server_connection.sendall(f"init\n{json_str}".encode('utf-8'))
            server_connection.close()
            return True
        except Exception as e:
            raise Exception(e)
        
    def shut_down(self):
        data = {
            'clientName': self.clientName,
            'serverHandlerPort': self.serverHandlerPort,
            'clientHandlerPort': self.clientHandlerPort,
            'repository': self.published_file
        }
        json_str = json.dumps(data, ensure_ascii=True)

        try:
            server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_connection.connect((self.serverIP, self.serverPort))
            server_connection.sendall(f"delete\n{json_str}".encode('utf-8'))
            server_connection.close()
            print("Notice deletion to server")
        except Exception as e:
            print("Cannot notice deletion to server")



if __name__ == '__main__':
    clientName = input("Client started. Please choose a name to display on the system: ")

    clientUI = ClientUI()

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.connect(("8.8.8.8", 80))
    serverIP = '192.168.1.10'
    clientIP = my_socket.getsockname()[0]
    my_socket.close()
    
    client = Client(serverInfo=(serverIP, 8000),
                    clientName=clientName, 
                    serverHandlerInfo=(clientIP, 0), 
                    clientHandlerInfo=(clientIP, 0),
                    SupplyingFile_number=10,
                    clientUI=clientUI)
    
    clientHandlerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientHandlerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientHandlerSocket.bind((clientIP, 0))
    clientHandlerSocket.listen(client.supplyingFile_number)
    # Take the port number
    _, clientHandlerPort = clientHandlerSocket.getsockname()
    serverHandlerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverHandlerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverHandlerSocket.bind((clientIP, 0))
    serverHandlerSocket.listen(1)
    # Take the port number
    _, serverHandlerPort = serverHandlerSocket.getsockname()
    
    # Sever Handler thread
    serverHandlerThread = threading.Thread(target=client.handle_server, args=(serverHandlerSocket,))
    serverHandlerThread.daemon = True
    serverHandlerThread.start()
    
    # Client Handler thread
    clientHandlerThread = threading.Thread(target=client.handle_client, args=(clientHandlerSocket,))
    clientHandlerThread.daemon = True
    clientHandlerThread.start()
    
    # tạo cái connection đến server và gửi các file cần thiết
    client.serverHandlerIP, client.serverHandlerPort = (clientIP, serverHandlerPort)
    client.clientHandlerIP, client.clientHandlerPort = (clientIP, clientHandlerPort)
    
    client.init_connection()

    client.handle_UI()
    client.shut_down()
