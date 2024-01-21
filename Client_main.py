from fastapi import FastAPI, Response, Request
import os
import socket
import signal
import threading

from Client_class import Client
from ClientAPI.FetchFile import fetch_file_owner, fetch_from_client, fetch_from_server
from ClientAPI.PublishFile import publish
from ClientAPI.ClientUI import ClientUI
from ClientAPI.DeleteFile import remove

from constant import *

import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
client = None
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/start/{name}")
def start_client(name: str):

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.connect(("8.8.8.8", 80))
    clientIP = my_socket.getsockname()[0]
    my_socket.close()

    global client
    client = Client(serverInfo=(SERVER_IP, SERVER_PORT),
                    clientName=name, 
                    serverHandlerInfo=(clientIP, 0), 
                    clientHandlerInfo=(clientIP, 0),
                    SupplyingFile_number=10,
                    clientUI=ClientUI())
    
    clientHandlerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientHandlerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientHandlerSocket.bind((clientIP, 0))
    clientHandlerSocket.listen(client.supplyingFile_number)

    # Take the port number of clientHandlerSocket
    _, clientHandlerPort = clientHandlerSocket.getsockname()

    serverHandlerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverHandlerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverHandlerSocket.bind((clientIP, 0))
    serverHandlerSocket.listen(1)

    # Take the port number of serverHandlerSocket
    _, serverHandlerPort = serverHandlerSocket.getsockname()

    # Start Sever Handler Thread
    serverHandlerThread = threading.Thread(target=client.handle_server, args=(serverHandlerSocket, ))
    serverHandlerThread.daemon = True
    serverHandlerThread.start()

    # Start Client Handler Thread
    clientHandlerThread = threading.Thread(target=client.handle_client, args=(clientHandlerSocket,))
    clientHandlerThread.daemon = True
    clientHandlerThread.start()

    # tạo cái connection đến server và gửi các file cần thiết
    client.serverHandlerIP, client.serverHandlerPort = (clientIP, serverHandlerPort)
    client.clientHandlerIP, client.clientHandlerPort = (clientIP, clientHandlerPort)
    
    # Start UI Handler Thread
    UIHandlerThread = threading.Thread(target=client.handle_UI)
    UIHandlerThread.daemon = True
    UIHandlerThread.start()

    client.init_connection()

    return {"Initialization_status": "Success"}

@app.get("/display")
def display_file():
    return client.published_file

@app.get("/fetch_from_server")
def fetch_files():
    return fetch_from_server(client.serverIP, client.serverPort)

@app.get("/fetch_file_owner/{fname}")
def fetch_owner(fname: str):
    return fetch_file_owner(client.serverIP, client.serverPort, fname)

@app.post("/fetch_from_client/{chosen_file}/{target_address}/{target_port}")
def download_file(chosen_file:str, target_address:str, target_port:int):
    target_info = {'address': target_address, 'port': target_port}
    download_result = fetch_from_client(chosen_file, client.repoPath, target_info)

    if download_result: client.published_file.append(chosen_file)

    if download_result == True: return {"download_status": "success"}
    else: return {"download_status": "failure"}

@app.post("/publish")
def publish_file(filepath:str, new_fileName:str):
    publish_result = publish(filepath, client.repoPath, new_fileName, client.serverIP, client.serverPort, client)

    if publish_result == True: 
        client.published_file.append(new_fileName)
        return {"publish_status": "success"}
    else: return {"publish_status": "failure"}

@app.post("/delete/{filename}")
def delete_file(filename:str):
    remove_result = remove(filename, client.repoPath, client.serverIP, client.serverPort, client)

    if remove_result == True: client.published_file.remove(filename)

    if remove_result == True: return {"remove_status": "success"}
    else: return {"remove_status": "failure"}

@app.post("/exit")
def Shutdown():
    client.shut_down()

    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Client shutting down...')

def calculate_average(data):
    total_time = sum(data)
    average_time = total_time / len(data)
    return average_time

def calculate_standard_deviation(data, average_time):
    squared_diff = sum((time - average_time) ** 2 for time in data)
    variance = squared_diff / len(data)
    standard_deviation = variance ** 0.5
    return standard_deviation

@app.get("/perform/{file_name}/{target_address}/{target_port}/{times}")
def performance_test(file_name: str, target_address:str, target_port:int, times:int):
    target_info = {'address': target_address, 'port': target_port}

    time_list = []
    for i in range(times):
        start = time.time()
        download_result = fetch_from_client(file_name, client.repoPath, target_info)
        end = time.time()
        if download_result == True:
            time_list.append(end - start)

    average_time = calculate_average(time_list)
    sd_time = calculate_standard_deviation(time_list, average_time)

    return {"average": average_time, "sd": sd_time}

@app.post('test')
async def test():
    # data = await request.json()
    # return {data}
    return {"test": "test"}