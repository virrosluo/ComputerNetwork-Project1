import socket
import json

def discover(clientInfo: dict) -> list[str]:
    r'''
    clientInfo: a dictionary format {'Address', 'Name', 'serverHandlerPort', 'ClientHandlerPort'}

    return a list of file name that get from this client
    '''

    # print(clientInfo['address'], clientInfo['serverHandlerPort'])
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((clientInfo['address'], clientInfo['serverHandlerPort']))
        connection.sendall("discover".encode())
        jsonStr = connection.recv(1024).decode()

        fileList = json.loads(jsonStr)
        print(fileList)
        return fileList
    except Exception as e:
        print("Error at discover in Server: ", e)
        return []