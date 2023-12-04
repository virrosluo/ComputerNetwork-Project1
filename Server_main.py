from fastapi import FastAPI, Response
import os
import signal

import socket
import threading

from ServerAPI.ServerUI import ServerUI
from ServerAPI.Discover import discover
from ServerAPI.Ping import ping

from Server_class import Server
from constant import *


app = FastAPI()
# uvicorn.run(app, port=8000, reload=True)

server = None

@app.get("/start")
def start_server():
    print("Call start server")
    global server
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.connect(("8.8.8.8", 80))
        serverIP = my_socket.getsockname()[0]
        my_socket.close()
        
        serverUI = ServerUI()
        server = Server(SERVER_IP, SERVER_PORT, 10, serverUI)

        clientHandlerThread = threading.Thread(target=server.client_handler)
        clientHandlerThread.daemon = True
        clientHandlerThread.start()

        commandHandlerThread = threading.Thread(target=server.UI_handler)
        commandHandlerThread.daemon = True
        commandHandlerThread.start()

        return {"initialization_status": "success"}
    except Exception as e:
        return {"initialization_status": e}
    
@app.get("/display")
def display_file():
    fileList = []

    for fname, clientList in server.available_file.items():
        fileList.append({fname: [server.clientDict[clientKey][0] for clientKey in clientList]})

    return fileList

@app.get("/getClient")
def get_client():
    r"""Use to return a list of client on UI for controller to choose which user will be ping"""

    clientList = [{'address':key[0], 'name':value[0], 'serverHandlerPort':key[1], 'clientHandlerPort':value[1]}
                  for key, value in server.clientDict.items()]
    print(clientList)
    
    return clientList

@app.get("/discover_file")
def discover_file(address:str, name:str, serverHandlerPort:int, clientHandlerPort:int):
    r"""Discover file to client x and return a list of files to Website"""

    clientInfo = {'address':address, 'name':name, 'serverHandlerPort':serverHandlerPort, 'clientHandlerPort':clientHandlerPort}
    file_list = discover(clientInfo=clientInfo)
    server.UpdateAvailableFile(file_list=file_list, clientInfo=clientInfo)

    return file_list

@app.get("/ping_client")
def ping_client(address:str, name:str, serverHandlerPort:int, clientHandlerPort:int):
    r"""Ping to client x and return the status of the client"""

    clientInfo = {'address':address, 'name':name, 'serverHandlerPort':serverHandlerPort, 'clientHandlerPort':clientHandlerPort}
    result = ping(clientInfo=clientInfo)
    if result == False: server.UpdateClientStatus(clientInfo)

    return {"client_status": result}

@app.post("/exit")
def Shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Server shutting down...')
