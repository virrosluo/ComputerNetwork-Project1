import socket
import os
import shutil
import json

def remove(fname:str, repoPath:str, serverIP, serverPort, clientInfo) -> bool:
    r"""
        Remove fname from the client Repo by Sending Remove Request to server, then pop the file out of repository
    """

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((serverIP, serverPort))
    except Exception as e:
        print("Cannot connect to server")
        return False
    
    # Send Remove request to server
    try:
        json_str = json.dumps({
            'fileName': fname,
            'name': clientInfo.clientName,
            'serverHandlerPort': clientInfo.serverHandlerPort,
            'clientHandlerPort': clientInfo.clientHandlerPort
        }, ensure_ascii=True)

        serverSocket.send(f"remove\n{json_str}".encode())
    except Exception as e:
        return False
    
    return pop_from_repo(fname, repoPath)


def pop_from_repo(fileName:str, repoPath:str) -> bool:
    r"""
        Pop a file out of repository
    """
    
    if os.path.exists(repoPath) == False: return False

    try:
        os.remove(os.path.join(repoPath, fileName))
        return True
    except Exception as e:
        print("Error:", e)
        return False