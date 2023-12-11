import socket
import os
import shutil
import json

def push_to_repo(filePath:str, repoPath:str, newFileName: str) -> bool:
    """
        Copy file from filePath to repoPath
    """
    if os.path.exists(repoPath) == False: os.mkdir(repoPath)

    try:
      shutil.copy2(filePath, os.path.join(repoPath, newFileName))
      return True
    except Exception as e:
       print("Cannot copy file at push_to_repo():", e)
       return False

def publish(fpath:str, repoPath:str, newFileName: str, serverIP, serverPort, clientInfo) -> bool:
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((serverIP, serverPort))
    except Exception as e:
        print("Cannot connect to server")
        return False

    if push_to_repo(fpath, repoPath, newFileName) == False: return False
    else:
        json_str = json.dumps({
            'fileName': newFileName,
            'name': clientInfo.clientName,
            'serverHandlerPort':clientInfo.serverHandlerPort,
            'clientHandlerPort':clientInfo.clientHandlerPort,
        }, ensure_ascii=True)

        serverSocket.send(f"publish\n{json_str}".encode())
        print(f"Publish file {fpath} and create a copy in repository with name {newFileName}")
        return True