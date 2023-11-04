import os
import socket
import json
import threading

from ClientAPI.FetchFile import *
from ClientAPI.PublishFile import *
from ClientAPI.ClientUI import *
from ClientAPI.SendFile import *

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

        self.ui = clientUI

        self.repoPath = 'repository'
        self.published_file = []
        if os.path.exists(self.repoPath):
            for fname in os.listdir(self.repoPath):
                print(fname)
                self.published_file.append(fname)

        self.init_connection()

    def handle_client(self):
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connectionSocket.bind((self.clientHandlerIP, self.clientHandlerPort))
        connectionSocket.listen(self.supplyingFile_number)

        while True:
            clientSocket, _ = connectionSocket.accept()
            task = threading.Thread(target=handle_fetch_request,
                                    args=(clientSocket, self.repoPath))
            task.start()
            
    def handle_server(self):
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connectionSocket.bind((self.serverHandlerIP, self.serverHandlerPort))
        connectionSocket.listen(1)

        while True:
            serverSocket, _ = connectionSocket.accept()
            
            msg = serverSocket.recv(1024).decode('utf-8')
            msg = msg.split(' ')

            if msg[0] == "discover":
                discover(serverSocket, self.published_file)
            elif msg[0] == "ping":
                pass

    def handle_UI(self):
        while True:
            command = input("Input command: ")
            command = command.split(' ')

            if command[0] == 'fetch':
                fetch(self.serverIP, self.serverPort, self.repoPath)
            elif command[0] == 'publish':
                publish(command[1], self.repoPath, self.serverIP, self.serverPort, self)
            else:
                print("Undefined command")

    def init_connection(self) -> bool:
        r'''
        Use to create the connection between the server and the client.
        Let the server know the information about the client
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
            raise Exception("Failed to init connection to server")
        
    def __del__(self):
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
    serverHandlerPort, clientHandlerPort = [int(port) for port in input("Input port: ").split(' ')]

    clientUI = ClientUI()
    client = Client(serverInfo=('192.168.1.153', 8000),
                    clientName='VirrosLuo', 
                    serverHandlerInfo=('192.168.1.153', serverHandlerPort), 
                    clientHandlerInfo=('192.168.1.153', clientHandlerPort),
                    SupplyingFile_number=10,
                    clientUI=clientUI)
    
    serverHandlerThread = threading.Thread(target=client.handle_server)
    serverHandlerThread.start()

    clientHandlerThread = threading.Thread(target=client.handle_client)
    clientHandlerThread.start()

    client.handle_UI()
