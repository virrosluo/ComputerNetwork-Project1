import socket
import json
import threading

from ServerAPI.ServerUI import ServerUI
from ServerAPI.Discover import *
from ServerAPI.Ping import *
from ServerAPI.SendFile import *
from ServerAPI.Publish import *

class Server:
    def __init__(self, 
                 IP_address, 
                 port, 
                 maxClient,
                 serverUI:ServerUI):

        self.IP_address = IP_address
        self.Port = port
        self.ui = serverUI
        self.maxClient = maxClient

        self.Stop_Thread = False

        # {key:('Address', 'ServerHandler') values: ('Name', 'ClientHandler')}
        self.clientDict = {}
        # Dictionary format: {'FileName': ['ClientName']}
        self.available_file = {}
        # Dictionary format: {'FileName': CursorIndex}
        self.index_list = {}

    def client_handler(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((self.IP_address, self.Port))
        serverSocket.listen(self.maxClient)

        while self.Stop_Thread == False:
            clientConnection, clientAddress = serverSocket.accept()
            msg = clientConnection.recv(1024).decode('utf-8')

            msg = msg.split('\n')

            if msg[0] == 'init':
                self.initHandler(clientAddress, msg[1])

            elif msg[0] == 'delete':
                self.deleteHandler(clientAddress, msg[1])

            elif msg[0] == 'fetch':
                handle_fetch(clientConnection, self.available_file, self.clientDict, self.index_list)

            elif msg[0] == 'publish':
                fname, key = handle_publish(clientAddress, msg[1])
                if fname not in self.available_file.keys(): self.push_fnameToDict(fname, key)
                else:
                    if key not in self.available_file[fname]: self.available_file[fname].append(key)

    def UpdateAvailableFile(self, file_list, clientInfo):
        r'''
        file_list: list of file name

        clientInfo: a dictionary format {'Address', 'Name', 'serverHandlerPort', 'ClientHandlerPort'}
        '''
        for fname in file_list:
            if fname not in self.available_file.keys():
                self.push_fnameToDict(fname, (clientInfo['address'], clientInfo['serverHandlerPort']))
            else:
                key = (clientInfo['address'], clientInfo['serverHandlerPort'])
                if key not in self.available_file[fname]:
                    self.available_file[fname].append(key)

    def UpdateClientStatus(self, clientInfo):
        r'''
        Input clientInfo and remove all this clientInfo from the server
        '''
        key = (clientInfo['address'], clientInfo['serverHandlerPort'])
        self.clientDict.pop(key)

        for fname, clientList in self.available_file.items():
            self.available_file[fname] = [clientKey for clientKey in clientList if clientKey != key]
            if self.available_file[fname] == []: self.pop_fnameFromDict(fname)

    def UI_handler(self):
        while self.Stop_Thread == False:
            command = input("Input command: ")
            command = command.split(' ')

            if command[0] == 'display':
                self.ui.display_publish_file(self.available_file, self.clientDict)

            elif command[0] == 'discover':
                discoverClient = self.get_client()
                file_list = discover(discoverClient)
                self.UpdateAvailableFile(file_list, discoverClient)

            elif command[0] == 'ping':
                discoverClient = self.get_client()
                result = ping(discoverClient)
                if result == False: self.UpdateClientStatus(discoverClient)
                self.ui.display_ping_info(result)

            elif command[0] == 'exit':
                self.Stop_Thread = True

            else: print("Undefined command")

    def get_client(self):
        r'''
        Let user choose the client and return that client Info to create the connection for next step
        '''
        clientList = [{'address':key[0], 'name':value[0], 'serverHandlerPort':key[1], 'clientHandlerPort':value[1]} 
                      for key, value in self.clientDict.items()]
        self.ui.display_available_client(clientList)
        index = int(input("Input the index client: "))
        return clientList[index]

    def initHandler(self, clientAddress, data):
        json_data = dict(json.loads(data))

        key = (clientAddress[0], json_data['serverHandlerPort'])
        self.clientDict[key] = (json_data['clientName'], 
                            json_data['clientHandlerPort'])
        
        for fname in json_data['repository']:
            if fname not in self.available_file.keys():
                self.push_fnameToDict(fname, key) 
            else: self.available_file[fname].append(key)

    def deleteHandler(self, clientAddress, data):
        json_data = dict(json.loads(data))

        key = (clientAddress[0], json_data['serverHandlerPort'])
        self.clientDict.pop(key)

        for fname in json_data['repository']:
            if fname not in self.available_file.keys():
                print("Has file not in available_file list when delete")
            else:
                self.available_file[fname] = [i for i in self.available_file[fname] if i != key]
                if self.available_file[fname] == []:
                    self.pop_fnameFromDict(fname)

    def pop_fnameFromDict(self, fname):
        r'''
        Use to remove a fname out of self.available_file and self.index_list
        '''
        if fname in self.available_file.keys(): self.available_file.pop(fname)
        else: print("Cannot pop out item from available_file", fname)

        if fname in self.index_list.keys(): self.index_list.pop(fname)
        else: print("Cannot pop out item from index_list", fname)
    
    def push_fnameToDict(self, fname, value): 
        r'''
        Use to push a fname into self.available_file and self.index_list
        '''
        self.available_file[fname] = [value]
        self.index_list[fname] = 0



if __name__ == '__main__':
    serverUI = ServerUI()
    server = Server('192.168.1.153', 8000, 10, serverUI)

    clientHandlerThread = threading.Thread(target=server.client_handler)
    clientHandlerThread.start()

    server.UI_handler()
