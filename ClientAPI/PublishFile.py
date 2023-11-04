import socket
import os
import shutil
import json

def push_to_repo(filePath:str, repoPath:str) -> bool:
    if os.path.exists(repoPath) == False: os.mkdir(repoPath)

    try:
      shutil.copy2(filePath, repoPath)
      return True
    except Exception as e:
       print("Cannot copy file at push_to_repo():", e)
       return False

def publish(fpath:str, repoPath:str, serverIP, serverPort, clientInfo) -> bool:
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((serverIP, serverPort))
    except Exception as e:
        print("Cannot connect to server")
        return False

    _, fname = os.path.split(fpath)
    if push_to_repo(fpath, repoPath) == False: return False
    else:
        json_str = json.dumps({
            'fileName': fname,
            'name': clientInfo.clientName,
            'serverHandlerPort':clientInfo.serverHandlerPort,
            'clientHandlerPort':clientInfo.clientHandlerPort,
        }, ensure_ascii=True)

        serverSocket.send(f"publish\n{json_str}".encode())
        return True